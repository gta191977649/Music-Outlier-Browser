import matplotlib.pyplot as plt
import numpy as np
from dissonant import harmonic_tone, dissonance, pitch_to_freq
from itertools import combinations

## TODO: ISSUE: Mach the vector mag to dissonance according to human perception
# Define the notes and their degrees in the circle of fifths
notes_degrees = {
    'C': 105, 'G': 75, 'D': 45, 'A': 15, 'E': -15, 'B': -45, 'F#': -75,
    'Db': -105, 'Ab': -135, 'Eb': -165, 'Bb': 165, 'F': 135
}

# Map the notes to their positions in the chromatic scale
notes_semitones = {
    'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11, 'F#': 6,
    'Db': 1, 'Ab': 8, 'Eb': 3, 'Bb': 10, 'F': 5
}

# Define the intervals within a major sixth (9 semitones)
intervals_within_sixth = list(range(1, 10))  # From one semitone above the root to major sixth

# A4 frequency for standard pitch
REFERENCE_FREQUENCY = 440

# Function to convert note names to frequencies
def note_to_frequency(note_name, reference_freq=440.0):
    # Distance of note from A in the chromatic scale
    semitone_distance_from_A = notes_semitones[note_name]
    # A4 is the 9th semitone from C in an octave, so we adjust by subtracting 9
    semitone_distance_from_A4 = semitone_distance_from_A - 9
    return reference_freq * (2 ** (semitone_distance_from_A4 / 12))

def note_from_root(root, semitones):
    root_position = notes_semitones[root]
    note_position = (root_position + semitones) % 12
    return [note for note, position in notes_semitones.items() if position == note_position][0]

def generate_chords_within_sixth(root):
    chords = []
    for combo in combinations(intervals_within_sixth, 2):  # Two additional notes forming a three-note chord
        chord_notes = [root] + [note_from_root(root, semitones) for semitones in combo]
        chords.append(chord_notes)
    return chords

def cartesian_to_polar(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)
    return r, np.degrees(theta)
def compute_chord_dissonance(chord_freqs, n_partials=10, model='sethares1993'):
    # Calculate the harmonic tones and their amplitudes for the given chord frequencies
    h_freqs, h_amps = harmonic_tone(chord_freqs, n_partials=n_partials)
    # Calculate the dissonance of the harmonic tones
    dissonance_value = dissonance(h_freqs, h_amps, model=model)
    return dissonance_value
def compute_chord_vectors(chord_notes, reference_freq=440.0, n_partials=10, model='sethares1993'):
    # Convert note names to frequencies
    freqs = [note_to_frequency(note, reference_freq) for note in chord_notes]
    # Calculate the dissonance of the chord
    dissonance_value = compute_chord_dissonance(freqs, n_partials=n_partials, model=model)
    # Convert dissonance value to a vector magnitude
    magnitude = 1 / (1 + dissonance_value)
    #magnitude = dissonance_value
    # Compute chord vectors using the magnitude
    chord_angles_rad = [np.deg2rad(notes_degrees[note]) for note in chord_notes]
    chord_vectors = np.array([np.cos(chord_angles_rad) * magnitude, np.sin(chord_angles_rad) * magnitude])
    # Sum the vectors to get the resultant vector for the chord
    sum_vector = np.sum(chord_vectors, axis=1)
    return sum_vector


def plot_model(chord_notes, sum_vector, ax):

    sum_vector_polar = cartesian_to_polar(sum_vector[0], sum_vector[1])
    ax.plot([0, np.deg2rad(sum_vector_polar[1])], [0, sum_vector_polar[0]], 'x', color='red')
    ax.plot([0, np.deg2rad(sum_vector_polar[1])], [0, sum_vector_polar[0]], '-', color="black", alpha=0.2)
    label = '-'.join(chord_notes)
    #ax.text(np.deg2rad(sum_vector_polar[1]), sum_vector_polar[0], label, fontsize=8, ha='left')

    return sum_vector_polar

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

total = 0

for root_note in notes_degrees:
    chords = generate_chords_within_sixth(root_note)
    print(root_note)
    for chord_notes in chords:
        sum_vector = compute_chord_vectors(chord_notes)
        sum_vector_polar = plot_model(chord_notes, sum_vector, ax)
        print(f"{chord_notes}: ({sum_vector_polar[0]},{sum_vector_polar[1]})")
        total += 1

# Circle of fifths line
sorted_notes = sorted(notes_degrees.items(), key=lambda x: x[1])
for i, ((note1, deg1), (note2, deg2)) in enumerate(zip(sorted_notes, sorted_notes[1:] + sorted_notes[:1])):
    angle1, angle2 = np.deg2rad(deg1), np.deg2rad(deg2)
    ax.plot([angle1, angle2], [1, 1], 'g-', linewidth=2)  # Connect the notes in the inner circle

for note, degree in notes_degrees.items():
    ax.plot(np.deg2rad(degree), 1, 'ro')  # Plot the position of each note
    ax.text(np.deg2rad(degree), 1.1, note, fontsize=10, ha='center')  # Label each note

ax.set_aspect('equal')
ax.set_rticks([])
ax.set_title(f"Full Chord Vector Distribution Map: Total {total}")

plt.show()
