from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import pandas as pd
import matplotlib.pyplot as plt
import h5.hdf5_getters as h5
import os
import music21

# NOTE THIS FILE READS A LAB CHORD FILE AND FEED IT INTO MODEL
# IT OUTPUTS THE VECTOR FROM INPUT CHORDS. IN THIS CASE GENERATES
# A SINGAL FROM IT.

def map_music21(chord_21,name):
    map_21 = {'A': eNote.A,
              'D': eNote.D,
              'G': eNote.G,
              'C': eNote.C,
              'F': eNote.F,
              'Bb': eNote.Bb,
              'A#': eNote.Bb,
              'Eb': eNote.Eb,
              'D#': eNote.Eb,
              'G#': eNote.Ab,
              'Ab': eNote.Ab,
              'C#': eNote.Db,
              'Db': eNote.Db,
              'F#': eNote.Fsharp,
              'Gb': eNote.Fsharp,
              'B': eNote.B,
              'E': eNote.E}
    temp = []
    for i in chord_21:
        temp.append(map_21[i])

    return VectorModel(temp,name=name)

def getChordVectorsFromFile(PATH_CHORD):
    chords = []
    with open(PATH_CHORD, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Skip the line if it starts with '#'
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) == 3:
                start, end, chord_str = parts
                # SKIP NONE CHORD
                if chord_str in ["N", "None"]: continue
                c = Chord(chord_str)
                notes = c.components()
                v = map_music21(notes, chord_str)
                chords.append({
                    "chord":v,
                    "start":start,
                    "end":end,
                })
    return chords
if __name__ == '__main__':
    # Chord File
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult"
    # Feed Chord Progression with Transposed or Original Key
    TRANSPOSED = True
    count = 0
    PATH_H5_DIR = os.path.join(BASE_PATH, "h5")
    for root, dirs, files in os.walk(PATH_H5_DIR):
        for filename in files:
            if os.path.splitext(filename)[1] == ".h5":
                # Check if chord lab file exits
                CHORD_FILENAME = filename.replace(".h5", TRANSPOSED and "_transposed.lab" or ".lab")
                PATH_CHORD = os.path.join(BASE_PATH, "chord", CHORD_FILENAME)
                if not os.path.exists(PATH_CHORD):
                    print("ERROR! {} Chord File Is Not Found!".format(CHORD_FILENAME))
                    continue
                # Do feed model, get vector model representation
                chords = getChordVectorsFromFile(PATH_CHORD)
                # Init attributes for Dataframe
                chord_name_ls = []
                chord_theta_ls = []
                chord_start_ls = []
                chord_end_ls = []
                for c in chords:
                    chord_name_ls.append(c["chord"].name)
                    chord_theta_ls.append(c["chord"].temp_theta)
                    chord_start_ls.append(c["start"])
                    chord_end_ls.append(c["end"])
                df = pd.DataFrame({
                    'chord_name': chord_name_ls,
                    'chord_theta': chord_theta_ls,
                    'start': chord_start_ls,
                    'end': chord_end_ls
                })
                #print(df)
                SONG_ID = os.path.splitext(CHORD_FILENAME)[0]

                OUTPUT_PATH_SIGNAL = os.path.join(BASE_PATH,"signal",SONG_ID+".csv")
                OUTPUT_PATH_DIR = os.path.join(BASE_PATH,"signal")
                if not os.path.exists(OUTPUT_PATH_DIR):
                    os.mkdir(OUTPUT_PATH_DIR)
                df.to_csv(OUTPUT_PATH_SIGNAL)
                count += 1
    print("ALL Done! Total: {} Songs.".format(count))







