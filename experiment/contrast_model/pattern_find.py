from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import pandas as pd
from tslearn.metrics import dtw_path,dtw
import os
from collections import defaultdict
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import h5.hdf5_getters as h5
import matplotlib.ticker as ticker

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

#TRSBHPR128F92C2C1D

def findChordPattern(PATH_CHORD,PATH_FILE):

    file = h5.open_h5_file_read(PATH_FILE)
    title = h5.get_title(file)
    chords = getChordVectorsFromFile(PATH_CHORD)

    chord_name_ls = []
    chord_theta_ls = []
    chord_start_ls = []
    chord_end_ls = []
    # Loop through Chords
    for c in chords:
        chord_name_ls.append(c["chord"].name)
        chord_theta_ls.append(c["chord"].temp_theta)
        chord_start_ls.append(float(c["start"]))
        chord_end_ls.append(float(c["end"]))

    # df = pd.DataFrame({
    #     'chord_name': chord_name_ls,
    #     'chord_theta': chord_theta_ls,
    #     'start': chord_start_ls,
    #     'end': chord_end_ls
    # })
    WINDOW = 4
    HOP_SIZE = 1  # Hop size of 1 allows overlapping windows
    matched_patterns = {}
    used_patterns = set()  # Set to keep track of unique patterns already used in a match

    for i in range(0, len(chord_theta_ls) - WINDOW + 1, HOP_SIZE):
        reference_signal = chord_theta_ls[i:i + WINDOW]
        pattern_key = tuple(chord_name_ls[i:i + WINDOW])  # Convert the pattern to a tuple to use it as a dictionary key

        if pattern_key not in used_patterns:
            used_patterns.add(pattern_key)  # Mark this pattern as used

            if pattern_key not in matched_patterns:
                matched_patterns[pattern_key] = {
                    'start_ref': i,
                    'end_ref': i + WINDOW - 1,
                    'matches': []
                }

            # Start the search loop from the end of the reference signal to avoid searching the reference signal itself
            for j in range(i + WINDOW, len(chord_theta_ls) - WINDOW + 1, HOP_SIZE):
                search_signal = chord_theta_ls[j:j + WINDOW]
                cost = dtw(reference_signal, search_signal)
                if cost == 0:
                    matched_patterns[pattern_key]['matches'].append({
                        'start_search': j,
                        'end_search': j + WINDOW - 1
                    })


    # Print All Found Matches

    output = []
    for pattern, details in matched_patterns.items():
        if len(details['matches']) > 0:
            output.append(pattern)
           # print(pattern,len(details['matches']))
    pattern_freq = {pattern: len(details['matches']) for pattern, details in matched_patterns.items() if
                    len(details['matches']) > 0}
    return output, title.decode('utf-8'),  pattern_freq


if __name__ == '__main__':
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/colin_meloy"
    TRANSPOSED = True
    PATH_H5_DIR = os.path.join(BASE_PATH, "h5")

    pattern_result = {}
    frequency_ls = []
    pattern_freq_total = defaultdict(int)

    for root, dirs, files in os.walk(PATH_H5_DIR):
        for idx, filename in enumerate(files):
            if os.path.splitext(filename)[1] == ".h5":
                CHORD_FILENAME = filename.replace(".h5", "_transposed.lab" if TRANSPOSED else ".lab")
                PATH_CHORD = os.path.join(BASE_PATH, "chord", CHORD_FILENAME)
                if not os.path.exists(PATH_CHORD):
                    print(f"ERROR! {CHORD_FILENAME} Chord File Is Not Found!")
                    continue
                PATH_FILE = os.path.join(root, filename)
                patterns,song_title,pattern_freq = findChordPattern(PATH_CHORD, PATH_FILE)
                for p in patterns:
                    if not p in pattern_result:
                        pattern_result[p] = []
                    pattern_result[p].append(song_title)
                    pattern_freq_total[p] += pattern_freq[p]
                print(f"PROCESSED: {CHORD_FILENAME}, {len(files) - idx} LEFT")
            # if idx == 10:
            #     break
    patterns_ls = []
    songcount_ls = []

    for pattern in pattern_result:
        patterns_ls.append(pattern)
        songcount_ls.append(len(pattern_result[pattern]))
        #print(pattern,len(pattern_result[pattern]))

    frequency_ls = [pattern_freq_total[p] for p in patterns_ls]
    df = pd.DataFrame({
        "pattern":patterns_ls,
        "songs":songcount_ls,
        "frequency": frequency_ls
    })
    df = df.sort_values(by='songs', ascending=False)

    df.to_csv("./pattern_song.csv")
    print(df)