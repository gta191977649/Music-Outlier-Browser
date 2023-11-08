import matplotlib.pyplot as plt
import numpy as np

# Setting up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Drawing the large rectangle for set M
ax.add_patch(plt.Rectangle((1, 1), 8, 4, fill=None, edgecolor='blue', linewidth=2))
ax.text(5, 5, "All Music Structures (M)", ha='center')

# Representing individual music structures
structures = ["Intro", "Verse", "Chorus", "Bridge", "Outro"]
x_coords = np.linspace(2, 8, len(structures))
for x, structure in zip(x_coords, structures):
    ax.add_patch(plt.Circle((x, 3), 0.5, fill=None, edgecolor='green', linewidth=1))
    ax.text(x, 3, structure, ha='center', va='center')

# Highlighting specific song structure m
ax.add_patch(plt.Circle((x_coords[2], 3), 0.5, fill=None, edgecolor='black', linewidth=2))
ax.text(x_coords[2], 4.5, "Song m Structure", ha='center', color='black')

# Adherence to M
adherence_lines = [0, 1, 3]
for index in adherence_lines:
    ax.plot([x_coords[2], x_coords[index]], [3, 3], color='grey', linestyle='--')

# Non-adherence threshold CG
ax.axhline(2, color='red', linestyle='dashed')
ax.text(0.5, 2, "Adherence Threshold ($C_G$)", va='center', color='red')

# Non-adherent song indicator
ax.text(x_coords[2], 1.5, "X", color='red', fontsize=15)

plt.show()
