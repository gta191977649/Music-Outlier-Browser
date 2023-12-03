import matplotlib.pyplot as plt
import numpy as np
from dissonant import harmonic_tone, dissonance, pitch_to_freq

# Define the scale and chords
scale_degrees = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]  # W-W-H-W-W-W-H

def compute_scale_chords(base_note, intervals):
    # Generate all scale notes
    scale_notes = [(base_note + interval) % 12 for interval in intervals]
    # Generate chords (triads for this example)
    chords = [scale_notes[i:]+scale_notes[:i+3-len(scale_notes)] for i in range(len(scale_notes))]
    return chords


def compute_dissonance_for_chords(chords):
    dissonances = []
    for chord in chords:
        freqs = [pitch_to_freq(note) for note in chord]
        print(freqs)
        amps = np.array([1.0] * len(freqs))
        h_freqs, h_amps = harmonic_tone(freqs)
        dissonance_value = dissonance(h_freqs, h_amps)
        dissonances.append(dissonance_value)
    return dissonances

def plot_dissonances(dissonances, scale_degrees):
    plt.plot(scale_degrees, dissonances, marker='o')  # Use marker to indicate each data point
    plt.xlabel('Chord')
    plt.ylabel('Dissonance')
    plt.title('Dissonance of Chords in the Scale')
    plt.grid(True)  # Optional: adds a grid to the plot
    plt.show()

if __name__ == '__main__':
    # Input the base note of the scale (C=0, C#=1, ..., B=11)
    base_note = 0  # C
    chords = compute_scale_chords(base_note, major_scale_intervals)
    dissonances = compute_dissonance_for_chords(chords)
    plot_dissonances(dissonances, scale_degrees)
