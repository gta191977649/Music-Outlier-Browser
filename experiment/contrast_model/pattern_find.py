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
import chordify.utils as chordify

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
                    "beat":end,
                })
    return chords

#TRSBHPR128F92C2C1D

def findChordPattern(PATH_CHORD,PATH_FILE):

    file = h5.open_h5_file_read(PATH_FILE)
    title = h5.get_title(file)
    file.close()

    chords = getChordVectorsFromFile(PATH_CHORD)
    chord_name_ls = []
    chord_theta_ls = []
    chord_start_ls = []
    chord_beat_ls = []
    # Loop through Chords
    for c in chords:
        chord_name_ls.append(c["chord"].name)
        chord_theta_ls.append(c["chord"].temp_theta)
        chord_start_ls.append(float(c["start"]))
        chord_beat_ls.append(float(c["beat"]))

    START_ON_DOWNBEAT = True
    WINDOW = 16
    HOP_SIZE = 1  # Hop size of 1 allows overlapping windows
    matched_patterns = {}
    used_patterns = set()  # Set to keep track of unique patterns already used in a match
    cost_threshold = 1
    matched_indices = set()  # Set to keep track of indices that have been matched

    i = 0
    while i < len(chord_theta_ls) - WINDOW + 1:
        reference_signal = chord_theta_ls[i:i + WINDOW]
        pattern_key = tuple(chord_name_ls[i:i + WINDOW])  # Convert the pattern to a tuple to use it as a dictionary key
        # Make sure we only start from downbeats
        if START_ON_DOWNBEAT:
            if not chord_beat_ls[i] == 1.0:
                i += HOP_SIZE
                continue
        if i in matched_indices:  # Skip if this index is part of a matched pattern
            i += HOP_SIZE
            continue

        if pattern_key not in matched_patterns:
            matched_patterns[pattern_key] = {
                'start_ref': i,
                'end_ref': i + WINDOW - 1,
                'matches': []
            }

            # Use a while loop for dynamic control over the index j
            j = i + WINDOW
            while j < len(chord_theta_ls) - WINDOW + 1:
                if j in matched_indices:  # Skip if this index is part of a matched pattern
                    j += HOP_SIZE
                    continue
                if START_ON_DOWNBEAT:
                    if not chord_beat_ls[j] == 1.0:
                        j += HOP_SIZE
                        continue

                search_signal = chord_theta_ls[j:j + WINDOW]
                path_length = len(reference_signal) + len(search_signal)

                cost = dtw(reference_signal, search_signal)
                # normalize cost
                cost = cost / path_length

                if cost < cost_threshold:
                    print(cost)
                    matched_patterns[pattern_key]['matches'].append({
                        'start_search': j,
                        'end_search': j + WINDOW - 1
                    })
                    matched_indices.update(range(j, j + WINDOW))  # Mark these indices as matched
                    j += WINDOW  # Skip current found chord position
                else:
                    j += HOP_SIZE  # Move to the next position

            # If the current pattern has one or more matches, mark the pattern as used
            if len(matched_patterns[pattern_key]['matches']) > 0:
                matched_indices.update(range(i, i + WINDOW))  # Mark these indices as matched
                i += WINDOW
                continue

        i += HOP_SIZE  # Move to the next position

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
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe"
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

    chord_ls = []
    songcount_ls = []

    for pattern in pattern_result:
        patterns_ls.append(pattern)
        songcount_ls.append(len(pattern_result[pattern]))
        chord_ls.append(chordify.format_chord_progression(pattern))
        print(chordify.format_chord_progression(pattern),len(pattern_result[pattern]))

    frequency_ls = [pattern_freq_total[p] for p in patterns_ls]
    df = pd.DataFrame({
        "pattern":patterns_ls,
        "chord":chord_ls,
        "songs":songcount_ls,
        "frequency": frequency_ls
    })
    df = df.sort_values(by='songs', ascending=False)

    df.to_csv("./pattern_song.csv",index=False)
    print(df)