from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
import os

class Chordify:
    def __init__(self,file):
        self.file = file
        self.beats = []
    def anlysis(self):
        dcp = DeepChromaProcessor()
        decode = DeepChromaChordRecognitionProcessor()
        chroma = dcp(self.file)
        chords = decode(chroma)
        return chords
    def getLabFile(self,chords):
        chordsArray = []
        chord_idx = 0
        lab_path = os.path.join(BASE_PATH, "chord")
        lab_file_path = os.path.join(lab_path, "{}.lab".format(filename))

        for beat_idx in range(len(self.beats) - 1):
            curr_beat_time, curr_beat = self.beats[beat_idx]
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