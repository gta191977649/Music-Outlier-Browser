import numpy as np
from fastdtw import fastdtw
from tslearn.metrics import dtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

# Define chords by their angle on the circle of fifths
C = 0       # C Major
G = 30      # G Major
D = 60      # D Major
A = 90      # A Major
E = 120     # E Major
B = 150     # B Major
F_sharp = 180  # F# Major
C_sharp = 210  # C# Major
G_sharp = 240  # G# Major
D_sharp = 270  # D# Major
A_sharp = 300  # A# Major
F = 330      # F Major

# Example chord progression 1: C -> G -> D -> A
chord_progression_1 = np.array([[C], [G], [D], [A]])  # Reshaped to 2-D

# Example chord progression 2: G -> D -> A -> E
chord_progression_2 = np.array([[G], [D], [A], [E]])  # Reshaped to 2-D

distance = dtw(chord_progression_1, chord_progression_2)
distance, path = fastdtw(chord_progression_1, chord_progression_2, dist=euclidean)

# If you have the path from fastdtw
path_x, path_y = zip(*path)
plt.plot(path_x, path_y)




# Add titles, labels if necessary
plt.title('DTW Alignment between two chord progressions')
plt.show()