from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
import os

# YOU SHOULD INPUT WAV FILE TO GET CHOED LABELS
BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/the_weather_girls"


def chord_recognition(file):
    dcp = DeepChromaProcessor()
    decode = DeepChromaChordRecognitionProcessor()
    chroma = dcp(file)
    chords = decode(chroma)
    return chords
def write_chord_file(filename,chords):
    lab_path = os.path.join(BASE_PATH, "chord")

    if not os.path.exists(lab_path):
        os.makedirs(lab_path)

    lab_file_path = os.path.join(lab_path, "{}.lab".format(filename))

    lab_file_content = ""
    for chord in chords:
        start, end, name = chord
        lab_file_content += "{}\t{}\t{}\n".format(start, end, name)

    with open(lab_file_path, "w") as f:
        f.write(lab_file_content)

    print("Processed: {}".format(filename))

if __name__ == '__main__':
    # BEGIN MAIN PROGRAM
    for root, dirs, files in os.walk(BASE_PATH+"/wav"):
        for filename in files:
            if os.path.splitext(filename)[1] == ".wav":
                path = os.path.join(root, filename)
                chords = chord_recognition(path)
                filename = filename.replace(".wav","")
                write_chord_file(filename,chords)