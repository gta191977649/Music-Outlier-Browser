from Chord import *
import matplotlib.pyplot as plt
import numpy as np


# Define the Circle of Fifths
circle_of_fifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

# Define the angles for each note in the Circle of Fifths (dividing the circle into 12 parts)
angles_circle_of_fifths = np.linspace(0, 2 * np.pi, len(circle_of_fifths), endpoint=False)

# Create a polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))

# Plot the chords in blue
for chord, (r, theta) in all_chord_coordinates().items():
    ax.scatter(theta, r, color='blue')  # Chord coordinates in blue

# Plot the Circle of Fifths labels
for label, angle in zip(circle_of_fifths, angles_circle_of_fifths):
    ax.text(angle, 11, label, ha='center', va='center', color='black', fontsize=20, backgroundcolor='white')

# Customize the plot
ax.grid(color='black')  # Grid in black
ax.set_facecolor('white')  # Background color to white
ax.set_theta_zero_location('N')  # Set the zero point to the top of the plot
ax.set_theta_direction(-1)  # Set the direction of increasing angles to clockwise

plt.show()