import matplotlib.pyplot as plt
import numpy as np

notes_degrees = {
    'C': 105, 'G': 75, 'D': 45, 'A': 15, 'E': -15, 'B': -45, 'F#': -75,
    'Db': -105, 'Ab': -135, 'Eb': -165, 'Bb': 165, 'F': 135
}
chord_notes = ['C', 'D', 'G']
def cartesian_to_polar(x, y):
    """Convert Cartesian coordinates to Polar coordinates."""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, np.degrees(theta)  # Radius and Angle in degrees
def plot_model(notes_degrees, chord_notes, ax):


    angles_rad = np.deg2rad(list(notes_degrees.values()))
    chord_angles_rad = [np.deg2rad(notes_degrees[note]) for note in chord_notes]
    # Sum Chord Vector
    chord_vectors = np.array([np.cos(chord_angles_rad), np.sin(chord_angles_rad)]).T
    sum_vector = np.sum(chord_vectors, axis=0)
    sum_vector_polar = cartesian_to_polar(*sum_vector)

    # Plot Model
    for angle_rad, note in zip(angles_rad, notes_degrees.keys()):
        ax.plot(angle_rad, 1, 'ro')
        ax.text(angle_rad, 1.2, note, fontsize=10, ha='center')

    # Plot Inner Circle
    sorted_notes = sorted(notes_degrees.items(), key=lambda x: x[1])
    for i, ((note1, deg1), (note2, deg2)) in enumerate(zip(sorted_notes, sorted_notes[1:] + sorted_notes[:1])):
        angle1, angle2 = np.deg2rad(deg1), np.deg2rad(deg2)
        ax.plot([angle1, angle2], [1, 1], 'g-', linewidth=2)

    # Plot Hited chord
    for angle_rad in chord_angles_rad:
        ax.plot([0, angle_rad], [0, 1], 'k-', linewidth=1)

    # Plot Result Vector
    ax.plot([0,np.arctan2(sum_vector[1], sum_vector[0])], [0, sum_vector_polar[0]], 'r-', linewidth=3)

    ax.set_aspect('equal')
    # ax.set_ylim(0, 1.5)
    ax.set_rticks([])
    legend_label = f'Chord Vector: (r={sum_vector_polar[0]:.2f}, θ={sum_vector_polar[1]:.2f}°)'
    ax.legend([legend_label])
    return sum_vector_polar

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
chord_vector = plot_model(notes_degrees, chord_notes, ax)
print("Chord Vector:({},{})".format(chord_vector[0],chord_vector[1]))
plt.show()


