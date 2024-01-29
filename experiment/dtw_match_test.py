import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tslearn.metrics import dtw_path,dtw
from collections import Counter

# Create two signals of different lengths
S_1 = pd.read_csv("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/test/蒲公英约定.csv")
S_2 = pd.read_csv("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/test/最长的电影.csv")
S_1 = np.array(S_1["chord_theta"])
S_2 = np.array(S_2["chord_theta"])


np.random.seed(0)
# signal1 = np.cos(np.linspace(0, 10, 100)) + np.random.normal(size=100) * 0.2
# signal2 = np.cos(np.linspace(0, 10, 150)) + np.random.normal(size=150) * 0.2
signal1 = S_1
signal2 = S_2
path, dist = dtw_path(signal1, signal2)


# Count how many times each index in signal1 and signal2 is used in the matching path
counter_signal1 = Counter(idx1 for idx1, idx2 in path)
counter_signal2 = Counter(idx2 for idx1, idx2 in path)

# Find indices in signal1 and signal2 with multiple matches
multiple_matches_signal1 = {idx for idx, count in counter_signal1.items() if count > 1}
multiple_matches_signal2 = {idx for idx, count in counter_signal2.items() if count > 1}

# Find indices in signal1 and signal2 with single matches
single_matches_signal1 = {idx for idx, count in counter_signal1.items() if count == 1}
single_matches_signal2 = {idx for idx, count in counter_signal2.items() if count == 1}

# Create a single plot
plt.figure(figsize=(20, 4))

# Plot signal1
plt.plot(signal1, label='Signal 1', drawstyle='steps-post')

# Shift signal2 downwards for clarity and plot
shift_down = 2 * np.max(signal1)  # Calculate a suitable shift value
plt.plot(np.arange(len(signal2)) * len(signal1) / len(signal2), signal2 - shift_down, label='Signal 2 (shifted down)', drawstyle='steps-post')

# Draw lines connecting the matched pairs
for idx1, idx2 in path:
    # Rescale idx2 to match the length of signal1 for visualization purposes
    idx2_rescaled = idx2 * len(signal1) / len(signal2)

    # Determine the color based on whether both points in the pair have single matches
    color = 'red' if (idx1 in single_matches_signal1 and idx2 in single_matches_signal2) else 'grey'

    plt.plot([idx1, idx2_rescaled], [signal1[idx1], signal2[idx2] - shift_down], color, alpha=0.6)  # Shift signal2 points down

plt.title('DTW Alignment between Signal 1 and Signal 2')
plt.legend()
plt.show()

