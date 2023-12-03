import numpy as np
import matplotlib.pyplot as plt
from dissonant import dissonance, harmonic_tone

# Base frequencies for the curves
base_note_freq = 130.8 # C3
base_frequencies = [base_note_freq * 2 ** i for i in range(0, 5)]
# Define the range of intervals in 12-TET steps
intervals = np.linspace(0, 12, 100)  # One octave
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']

# Function to convert 12-TET steps to frequency ratio
def steps_to_ratio(steps):
    return 2 ** (steps / 12)

# Calculate dissonance for each base frequency across intervals
for base_f in base_frequencies:
    dissonances = []
    for interval in intervals:
        freq1 = base_f
        freq2 = base_f * steps_to_ratio(interval)
        # Generate harmonic tones for two frequencies
        h_freqs, h_amps = harmonic_tone([freq1, freq2])
        # Calculate dissonance
        d = dissonance(h_freqs, h_amps,model="sethares1993")
        dissonances.append(d)

    # Plot the dissonance curve for this base frequency
    plt.plot(intervals, dissonances, label=f"{base_f} Hz")

# Customize and display the plot
plt.xticks(np.linspace(0, 12, 13), note_names)  # Set note names as x-axis labels
plt.xlabel('Scale')
plt.ylabel('Sensory dissonance')
plt.title('Sensory Dissonance Curves')
plt.legend()
plt.grid(True)
plt.show()
