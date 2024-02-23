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
from chordify import feature_extractor as feature

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
                chord_str = chord_str.replace(":","")
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

def summaryChordPattern(PATH_CHORD):


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

    START_ON_DOWNBEAT = True  # Set algorithm to only start search on chord that is on downbeat
    WINDOW = 16  # measures for chord progession length
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
                    #print(cost)
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
            output.append({
                "pattern": pattern,
                "matches": len(details['matches']),
            })
           # print(pattern,len(details['matches']))
    #pattern_freq = {pattern: len(details['matches']) for pattern, details in matched_patterns.items() if len(details['matches']) > 0}

    return output


if __name__ == '__main__':
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/abba"
    TRANSPOSED = True
    PATH_CHORD = os.path.join(BASE_PATH, "chord")
    PATH_META = os.path.join(BASE_PATH, "meta.csv")
    PATH_PATTERN = os.path.join(BASE_PATH, "pattern")

    pattern_result = {}
    frequency_ls = []
    pattern_freq_total = defaultdict(int)

    chord_pattern_summary = []

    files = pd.read_csv(PATH_META)
    for idx, song in files.iterrows():
        song_title = song["title"]
        mode = song["mode"] == "major"
        CHORD_FILENAME = os.path.join(PATH_CHORD, song_title.replace(".mp3", "_transposed.lab" if TRANSPOSED else ".lab"))

        if os.path.exists(CHORD_FILENAME):
            patterns = summaryChordPattern(CHORD_FILENAME)

            for p in patterns:
                roman = feature.chord_to_roman(p["pattern"],is_major=mode)
                p["roman_number"] = roman
            chord_pattern_summary.append({
                "title":song_title,
                "mode": song["mode"],
                "patterns": patterns,
            })
            # for p in patterns:
            #     if not p in pattern_result:
            #         pattern_result[p] = []
            #     # = feature.chord_to_roman(p,mode)
            #     pattern_result[p].append(song_title)
            #     pattern_freq_total[p] += pattern_freq[p]
            print(f"PROCESSED: {CHORD_FILENAME}, {len(files) - idx} LEFT")
    #print(chord_pattern_summary)


    for song in chord_pattern_summary:
        title = song["title"]
        mode = song["mode"]
        patterns = song["patterns"]

        pattern_ls = []
        transition_ls = []
        frequency_ls = []
        for pattern in patterns:
            pattern_ls.append(pattern["pattern"])
            frequency_ls.append(pattern["matches"])
            transition_buffer = []
            current_transition = None
            for chord in pattern["pattern"]:
                if not chord == current_transition:
                    transition_buffer.append(chord)
                    current_transition = chord
            transition_ls.append(transition_buffer)


        df = pd.DataFrame({
            "patterns": pattern_ls,
            "transitions": transition_ls,
            "frequency": frequency_ls,
        })
        if not os.path.exists(PATH_PATTERN): os.makedirs(PATH_PATTERN)
        df.to_csv(os.path.join(PATH_PATTERN,title.replace(".mp3",".csv")), index=False)
    # patterns_ls = []
    #
    # chord_ls = []
    # songcount_ls = []
    #
    # for pattern in pattern_result:
    #     patterns_ls.append(pattern)
    #     songcount_ls.append(len(pattern_result[pattern]))
    #     chord_ls.append(chordify.format_chord_progression(pattern))
    #     print(chordify.format_chord_progression(pattern),len(pattern_result[pattern]))
    #
    # frequency_ls = [pattern_freq_total[p] for p in patterns_ls]
    # df = pd.DataFrame({
    #     "pattern": patterns_ls,
    #     "chord": chord_ls,
    #     "associated_songs": songcount_ls,
    #     "frequency": frequency_ls
    # })
    # df = df.sort_values(by='frequency', ascending=False)
    #
    # OUTPUT_PATH = os.path.join(BASE_PATH,"pattern_song.csv")
    # df.to_csv(OUTPUT_PATH,index=False)
    # print(df)