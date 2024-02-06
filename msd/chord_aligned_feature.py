import os
import sys
import time
import glob
import matplotlib.pyplot as plt
import numpy as np
import h5.hdf5_getters as h5
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import librosa
def get_chord_time_warp_matrix(chord_starts, btstarts, chord_lengths, duration):
    warpmat = np.zeros((len(chord_starts), len(btstarts)))

    for n in range(len(btstarts)):
        start = btstarts[n]
        end = start + (btstarts[n + 1] - start) if n + 1 < len(btstarts) else duration

        try:
            start_idx = np.nonzero((chord_starts - start) >= 0)[0][0] - 1
        except IndexError:
            break

        chord_after = np.nonzero((chord_starts - end) >= 0)[0]
        end_idx = chord_after[0] if chord_after.shape[0] > 0 else start_idx

        warpmat[start_idx:end_idx, n] = 1.
        warpmat[start_idx, n] = 1. - ((start - chord_starts[start_idx]) / chord_lengths[start_idx])
        if end_idx - 1 > start_idx:
            warpmat[end_idx - 1, n] = ((end - chord_starts[end_idx - 1]) / chord_lengths[end_idx - 1])
        warpmat[:, n] /= np.sum(warpmat[:, n])

    return warpmat.T


def get_chord_start(file_path):
    """
    Parses a chord file with the format "start_time\tend_time\tchord".

    Parameters:
    - file_path: Path to the chord file.

    Returns:
    - chord_starts: List of start times for each chord.
    - chord_labels: List of chord labels.
    """
    chord_starts = []
    chord_labels = []

    with open(file_path, 'r') as file:
        for line in file:
            if '\t' not in line:
                continue

            if line.startswith("#"):
                continue

            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue

            start_time, _, chord = parts
            try:
                chord_starts.append(float(start_time))
                chord_labels.append(chord)
            except ValueError:
                print(f"Warning: Invalid start time '{start_time}' in line: {line.strip()}")

    return chord_starts, chord_labels


def visualize_beat_chord_grid_colored(beat_aligned_chord_names, btstarts, time_sig, bars_per_row=4):
    # Create a color map for chords
    unique_chords = list(set(beat_aligned_chord_names))
    color_map = plt.get_cmap('tab20')(np.linspace(0, 1, len(unique_chords)))
    chord_to_color = dict(zip(unique_chords, color_map))

    # Calculate the total number of bars and beats
    num_beats = len(beat_aligned_chord_names)
    num_bars = (num_beats + time_sig - 1) // time_sig  # Round up to the nearest whole bar

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, (num_bars // bars_per_row + 1) * 2))  # Dynamic height based on number of bars

    # Plot each beat and its corresponding chord
    for beat_idx, chord in enumerate(beat_aligned_chord_names):
        bar_idx = beat_idx // time_sig
        row = bar_idx // bars_per_row
        col = bar_idx % bars_per_row
        beat_in_bar = beat_idx % time_sig

        chord_color = chord_to_color[chord]

        # Draw a colored box for each beat
        beat_rect = patches.Rectangle((col * (time_sig + 1) + beat_in_bar, row), 1, 1, linewidth=1,
                                      edgecolor='black', facecolor=chord_color)
        ax.add_patch(beat_rect)

        # Label chord in the center of the bar
        if beat_in_bar == 0 or chord != beat_aligned_chord_names[beat_idx - 1]:
            ax.text(col * (time_sig + 1) + beat_in_bar + 0.5, row + 0.5, chord, ha='center', va='center',
                    color='black', fontsize=10)

    # Set the limits and labels
    ax.set_xlim(0, bars_per_row * (time_sig + 1))
    ax.set_ylim(0, (num_bars + bars_per_row - 1) // bars_per_row)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title('Chord Progression and Beats (Grouped by Time Signature)')
    ax.invert_yaxis()  # Invert y-axis so bars start from top

    # Create a custom legend for chord colors
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color=chord_to_color[chord], lw=4, label=chord) for chord in unique_chords]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.1, 1))

    plt.tight_layout()  # Adjust layout to fit all elements
    plt.show()
if __name__ == '__main__':
    file = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/h5/TRPSSSL128F4267C28.h5"
    chord_starts, chord_labels = get_chord_start("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/msd/beat_track.mp3.lab")
    song = h5.open_h5_file_read(file)
    duration = h5.get_duration(song)
    chord_lengths = np.concatenate((chord_starts[1:], [duration])) - chord_starts
    btstarts = h5.get_beats_start(song)
    bar_starts = h5.get_bars_start(song)
    time_sin = h5.get_time_signature(song)


    warp_matrix = get_chord_time_warp_matrix(chord_starts, btstarts, chord_lengths, duration)
    chord_indices = np.arange(len(chord_labels))
    beat_aligned_chords = np.dot(warp_matrix, chord_indices)
    beat_aligned_chord_names = [chord_labels[int(round(idx))] for idx in beat_aligned_chords]

    visualize_beat_chord_grid_colored(beat_aligned_chord_names, btstarts, 4,4)
