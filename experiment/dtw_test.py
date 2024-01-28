import numpy as np
from dtaidistance import dtw
import matplotlib.pyplot as plt

# Example signals
signal1 = np.sin(np.linspace(0, 20, 200)) + np.random.normal(0, 0.1, 200)
signal2 = np.sin(np.linspace(0, 20, 200) + 1) + np.random.normal(0, 0.1, 200)  # Slightly out of phase

# Parameters
window_size = 20
hop_size = 10

# Store the DTW distances
distances = []

# Iterate over the signals
for i in range(0, len(signal1) - window_size + 1, hop_size):
    # Define the window
    window1 = signal1[i:i + window_size]
    window2 = signal2[i:i + window_size]

    # Calculate DTW distance
    distance = dtw.distance(window1, window2)
    distances.append(distance)

# Plotting the signals and distances
plt.figure(figsize=(12, 6))

# Plot signal1
plt.subplot(3, 1, 1)
plt.plot(signal1, label='Signal 1')
plt.title('Signal 1')
plt.legend()

# Plot signal2
plt.subplot(3, 1, 2)
plt.plot(signal2, label='Signal 2')
plt.title('Signal 2')
plt.legend()

# Plot DTW distances
plt.subplot(3, 1, 3)
plt.plot(range(0, len(signal1) - window_size + 1, hop_size), distances, label='DTW Distance')
plt.title('DTW Distance between windows')
plt.xlabel('Time')
plt.ylabel('Distance')
plt.legend()

plt.tight_layout()
plt.show()
