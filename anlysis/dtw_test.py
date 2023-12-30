import numpy as np
import matplotlib.pyplot as plt
from dtaidistance import dtw

def plot_similar_subsequences(signal_1, signal_2, max_distance_threshold):
    # Compute the DTW distance between the two signals
    dtw_distance = dtw.distance(signal_1, signal_2)

    plt.figure(figsize=(12, 6))

    # Plot the original signals
    plt.plot(signal_1, label='Signal 1', marker='o')
    plt.plot(signal_2, label='Signal 2', marker='x')

    # Check if the DTW distance is below the threshold
    print(dtw_distance)
    if dtw_distance < max_distance_threshold:
        # If similar, plot the entire signals in red as an indication
        plt.plot(signal_1, color='red', linewidth=2)
        plt.plot(signal_2, color='red', linewidth=2)

    plt.title("DTW Distance Between Two Signals")
    plt.xlabel("Time Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()

# Example usage
signal_1 = np.array([1, 2, 3, 4, 2, 1])
signal_2 = np.array([2, 3, 4, 5, 3, 2])
plot_similar_subsequences(signal_1, signal_2, max_distance_threshold=3.0)
