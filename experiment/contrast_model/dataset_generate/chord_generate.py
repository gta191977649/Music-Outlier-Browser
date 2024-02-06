from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor,CRFChordRecognitionProcessor,CNNChordFeatureProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
from madmom.features.downbeats import RNNDownBeatProcessor,DBNDownBeatTrackingProcessor

import os

# YOU SHOULD INPUT WAV FILE TO GET CHOED LABELS
BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult"


def chord_recognition(file):
    # detect chord
    dcp = DeepChromaProcessor()
    decode = DeepChromaChordRecognitionProcessor()
    chroma = dcp(file)
    chords = decode(chroma)
    # detect beats
    beat_processor = RNNDownBeatProcessor()
    beat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)
    beats = beat_decoder(beat_processor(file))
    return chords,beats
def write_chord_file(filename,chords,beats):
    # lab_path = os.path.join(BASE_PATH, "chord")
    #
    # if not os.path.exists(lab_path):
    #     os.makedirs(lab_path)
    #
    # lab_file_path = os.path.join(lab_path, "{}.lab".format(filename))
    #
    # lab_file_content = ""
    # for chord in chords:
    #     start, end, name = chord
    #     lab_file_content += "{}\t{}\t{}\n".format(start, end, name)
    #
    # with open(lab_file_path, "w") as f:
    #     f.write(lab_file_content)
    # generate chord with beats aligned
    chordsArray = []
    chord_idx = 0
    lab_path = os.path.join(BASE_PATH, "chord")
    lab_file_path = os.path.join(lab_path, "{}.lab".format(filename))
    for beat_idx in range(len(beats) - 1):
        curr_beat_time, curr_beat = beats[beat_idx]
        # find the corresponding chord for this beat
        while chord_idx < len(chords):
            chord_time, _, _ = chords[chord_idx]
            prev_beat_time, _ = (0, 0) if beat_idx == 0 else beats[beat_idx - 1]
            eps = (curr_beat_time - prev_beat_time) / 2
            if chord_time > curr_beat_time + eps:
                break
            chord_idx += 1

        # append to array
        _, _, prev_chord = chords[chord_idx - 1]
        chord = (curr_beat_time, curr_beat, prev_chord)

        chordsArray.append(chord)

    # Generate chord label file
    lab_file = ""
    for c in chordsArray:
        curr_beat_time, curr_beat, prev_chord = c
        print(curr_beat_time, curr_beat, prev_chord)
        lab_file += "{}\t{}\t{}\n".format(curr_beat_time, curr_beat, prev_chord)

    bts = []
    for b in beats:
        bts.append(b[0])

    f = open(lab_file_path , "w")
    f.write(lab_file)
    f.close()

    print("✅Processed: {}".format(filename))

if __name__ == '__main__':
    # BEGIN MAIN PROGRAM
    for root, dirs, files in os.walk(BASE_PATH+"/wav"):
        for idx,filename in enumerate(files):
            if os.path.splitext(filename)[1] == ".wav":
                path = os.path.join(root, filename)
                print("📃Processing: {}\n⌚️{} Left".format(path,len(files)-idx))
                chords,beats = chord_recognition(path)
                filename = filename.replace(".wav","")
                write_chord_file(filename,chords,beats)