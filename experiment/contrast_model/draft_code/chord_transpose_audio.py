import os.path

from pychord.constants import NOTE_VAL_DICT
from pychord import Chord
import h5.hdf5_getters as h5

INDEX_NOTE_DICT = {v: k for k, v in NOTE_VAL_DICT.items()}

def calculate_transpose_amount(original_key, original_mode):
    # Define target keys for Major (C) and Minor (Am)
    target_major = "C"
    target_minor = "A"

    # Get semitone value for original key and target keys
    original_key_val = NOTE_VAL_DICT[original_key]
    target_major_val = NOTE_VAL_DICT[target_major]
    target_minor_val = NOTE_VAL_DICT[target_minor]

    # Calculate transpose amount based on mode
    if original_mode == 1:  # Major
        transpose_amount = target_major_val - original_key_val
    elif original_mode == 0:  # Minor
        transpose_amount = target_minor_val - original_key_val
    else:
        raise ValueError("Mode should be 1 (Major) or 0 (Minor)")

    return transpose_amount

def transpose_chord_progression(data,input_file, output_file, transpose_amount):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    transposed_lines = []
    title = data["title"]
    key = data["key"]

    transposed_lines.append("#Song:{}, Key:{}, Transpose: {}\n".\
                            format(title,key,transpose_amount))
    for line in lines:
        parts = line.strip().split("\t")
        if len(parts) == 3:
            start, end, chord_str = parts
            if chord_str not in ["N", "None"]:  # Skip 'no chord' sections and 'None'
                chord_str = chord_str.replace(":", "")
                try:
                    chord = Chord(chord_str)
                    chord.transpose(transpose_amount)
                    transposed_chord = chord
                    transposed_line = "\t".join([start, end, str(transposed_chord)])
                except ValueError as e:
                    print(f"Error processing chord: {chord_str}. Error: {e}")
                    transposed_line = "\t".join([start, end, "None"])  # Placeholder for unrecognized chords
            else:
                transposed_line = "\t".join([start, end, chord_str])
            transposed_lines.append(transposed_line)
        else:
            print(f"Line format issue: {line}")

    # Print transposed lines for now (can be changed to write to file)
    #print(transposed_lines)
    with open(output_file, 'w') as file:
        for line in transposed_lines:
            file.write(line + "\n")

if __name__ == '__main__':
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/similar_song"
    # PATH_H5 = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/h5/TRZARJQ128F42679C9.h5"
    # PATH_CHORD = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/chord/TRZARJQ128F42679C9.lab"
    #
    SONG_KEY = {
        '擱淺.mp3':"F",
        '最長的電影.mp3':"E",
        '蒲公英的约定.mp3':"C",
    }
    PATH_H5_DIR = os.path.join(BASE_PATH,"wav")
    for root, dirs, files in os.walk(PATH_H5_DIR):
        for filename in files:
            PATH_CHORD = os.path.join(BASE_PATH, "chord", filename + ".lab")
            if os.path.exists(PATH_CHORD):
                title = filename
                key = SONG_KEY[title]
                output_file = PATH_CHORD.rsplit('.lab', 1)[0] + '_transposed.lab'
                transpose_amount = calculate_transpose_amount(key, 1)
                transpose_chord_progression({
                    "title":title,
                    "key":key,
                }, PATH_CHORD, output_file, transpose_amount)
                print("Processed: {}".format(title))