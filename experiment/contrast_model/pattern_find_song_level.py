import pychord

from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import pandas as pd
from tslearn.metrics import dtw_path,dtw
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import h5.hdf5_getters as h5
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
                start, beat, chord_str = parts
                # SKIP NONE CHORD
                if chord_str in ["N", "None"]: continue

                chord_str = chord_str.replace(":", "")

                c = Chord(chord_str)
                notes = c.components()
                v = map_music21(notes, chord_str)
                chords.append({
                    "chord":v,
                    "start":start,
                    "beat":beat,
                })
    return chords

#TRSBHPR128F92C2C1D

ARTIST = "blue_oyster_cult"
SONG_ID = "TRPSSSL128F4267C28"
# Chord File
#PATH_CHORD = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/{}/chord/{}.lab".format(ARTIST, SONG_ID)
PATH_CHORD = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/music/final_countdown.mp3.lab"
PATH_FILE = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/{}/h5/{}.h5".format(ARTIST, SONG_ID)

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
    chord_end_ls.append(float(c["beat"]))

df = pd.DataFrame({
    'chord_name': chord_name_ls,
    'chord_theta': chord_theta_ls,
    'start': chord_start_ls,
    'beat': chord_end_ls
})
WINDOW = 16
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
            print(cost)
            if cost == 0:
                matched_patterns[pattern_key]['matches'].append({
                    'start_search': j,
                    'end_search': j + WINDOW - 1
                })

# Plotting the signal
x_values = range(len(df))
filtered_patterns = {pattern: details for pattern, details in sorted(matched_patterns.items(), key=lambda item: len(item[1]['matches']), reverse=True) if len(details['matches']) > 0}

total_pattern_groups = len(filtered_patterns)

colormap = plt.cm.get_cmap('tab10', total_pattern_groups)  # 'tab10' has a wide range of distinct colors

color_idx = 0

fig, axs = plt.subplots(total_pattern_groups, 1, figsize=(15, 2 * total_pattern_groups), squeeze=True)
axs = axs.flatten()

# Plot each unique pattern and its matches in a separate subplot
for (pattern, details), ax in zip(filtered_patterns.items(), axs):
    # Get color from the colormap, use modulo to cycle through colors if there are more patterns than colors
    color = colormap(color_idx % colormap.N)
    color_idx += 1  # Increment color index for the next distinct pattern

    # Plot the entire signal in a neutral color in the background
    neutral_color = 'grey'
    ax.plot(x_values, df['chord_theta'], marker='o', alpha=0.5, color=neutral_color, drawstyle='steps-post', markersize=2, zorder=1)

    # Reference pattern segment
    ref_start_idx = details['start_ref']
    ref_end_idx = details['end_ref']
    ax.plot(x_values[ref_start_idx:ref_end_idx + 1], df['chord_theta'][ref_start_idx:ref_end_idx + 1], marker='o',
            color=color, drawstyle='steps-post', markersize=2, zorder=2, label='Reference')

    # Plot each matching segment
    for match in details['matches']:
        search_start_idx = match['start_search']
        search_end_idx = match['end_search']
        ax.plot(x_values[search_start_idx:search_end_idx + 1], df['chord_theta'][search_start_idx:search_end_idx + 1],
                marker='o',linewidth=3, color=color, drawstyle='steps-post', markersize=2, zorder=2, label='Match')

    # Set title and labels for each subplot
    ax.set_title(f"Pattern: {pattern} - {len(details['matches'])} Matches")
    ax.set_ylabel('Angle')
    ax.set_xticks(x_values)
    ax.set_xticklabels(df['beat'], rotation='vertical', fontsize=8)
    ax.set_xlim(left=0, right=max(x_values))
    ax.set_ylim(min(df['chord_theta']), max(df['chord_theta']))
    ax.legend()

# Finalizing the plot
plt.tight_layout()
plt.show()

# Print All Found Matches
for pattern, details in matched_patterns.items():
    if len(details['matches']) > 0:
        print(pattern,len(details['matches']))