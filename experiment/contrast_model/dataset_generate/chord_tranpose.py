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

def transpose_chord_progression(h5_file,input_file, output_file, transpose_amount):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    transposed_lines = []

    title = h5.get_title(h5_file)
    key_name = INDEX_NOTE_DICT[key_index]
    key_conf = h5.get_key_confidence(h5_file)
    mode = h5.get_mode(h5_file)
    mode_conf = h5.get_mode_confidence(h5_file)
    mode_name = mode == 1 and "C Major" or "A Minor"
    transposed_lines.append("#Song:{}, Key:{}, Key Confidence:{}, Mode:{}, Mode Confidence:{},Transpose: {} to {}\n".\
                            format(title,key_name,key_conf,mode,mode_conf,transpose_amount,mode_name))
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
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe_aud"
    # PATH_H5 = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/h5/TRZARJQ128F42679C9.h5"
    # PATH_CHORD = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/chord/TRZARJQ128F42679C9.lab"

    PATH_H5_DIR = os.path.join(BASE_PATH,"h5")
    for root, dirs, files in os.walk(PATH_H5_DIR):
        for filename in files:
            if os.path.splitext(filename)[1] == ".h5":
                # Check if chord lab file exits
                CHORD_FILENAME = filename.replace(".h5",".lab")
                PATH_CHORD = os.path.join(BASE_PATH,"chord",CHORD_FILENAME)
                if not os.path.exists(PATH_CHORD):
                    print("ERROR! {} Chord File Is Not Found!".format(CHORD_FILENAME))
                    continue
                PATH_H5 = os.path.join(root,filename)
                # Transpose Chord Progression For each song
                file = h5.open_h5_file_read(PATH_H5)
                title = h5.get_title(file)
                key_index = h5.get_key(file)
                key_conf = h5.get_key_confidence(file)
                # !!!!!!! VERY IMPORTANT NOTE !!!!!!!
                # Mode indicates the modality (major or minor) of a track,
                # Major is represented by 1 and minor is 0. (FUCK SAKE, PEOPLE NORMALLY
                # WOULD THINK 0 is MAJOR 1 IS MINOR!!! Make sure value is CORRECT!!!!
                mode = h5.get_mode(file)
                mode_conf = h5.get_mode_confidence(file)
                key_name = INDEX_NOTE_DICT[key_index]

                transpose_amount = calculate_transpose_amount(key_name, mode)
                output_file = PATH_CHORD.rsplit('.lab', 1)[0] + '_transposed.lab'

                transpose_chord_progression(file,PATH_CHORD,output_file, transpose_amount)
                file.close()
                print("Processed: {}:Key:{},Mode:{},Tranpose Amount:{}".format(title,key_name,mode,transpose_amount))