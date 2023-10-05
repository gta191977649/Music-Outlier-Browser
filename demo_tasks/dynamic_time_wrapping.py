# Importing the required libraries
from tslearn.metrics import dtw_path
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import numpy as np

# Creating two example time series
t = np.linspace(0, 6.28, 100)
noise = np.random.normal(0, 0.1,100)  # noise with mean=0 and std=0.1
time_series_1 = np.sin(t)
time_series_2 = np.sin(t+noise)

# Reshaping to meet the input shape requirement for dtw_path
time_series_1 = time_series_1.reshape(-1, 1)
time_series_2 = time_series_2.reshape(-1, 1)

# Calculating the DTW path
path, sim = dtw_path(time_series_1, time_series_2)

print(f"DTW Distance: {sim}")
# Extracting the path coordinates
path_1 = [i[0] for i in path]
path_2 = [i[1] for i in path]

# Creating the similarity matrix (distance matrix)
similarity_matrix = cdist(time_series_1, time_series_2)

# Creating the figure and subplots
plt.figure(1, figsize=(8, 8))

# Definitions for the axes
left, bottom = 0.01, 0.1
w_ts = h_ts = 0.2
left_h = left + w_ts + 0.02
width = height = 0.65
bottom_h = bottom + height + 0.02

rect_s_y = [left, bottom, w_ts, height]
rect_gram = [left_h, bottom, width, height]
rect_s_x = [left_h, bottom_h, width, h_ts]

ax_gram = plt.axes(rect_gram)
ax_s_x = plt.axes(rect_s_x)
ax_s_y = plt.axes(rect_s_y)

# Plotting the similarity matrix with the DTW path
ax_gram.imshow(similarity_matrix, cmap='gray_r', origin='lower')
ax_gram.set_xlabel('Reference Signal (sin(t))')
ax_gram.set_ylabel('Dependent Signal (cos(t))')
ax_gram.plot(path_2, path_1, 'r-', linewidth=3.)  # Changed 'w-' to 'r-' for red color

# Plotting the reference signal (time_series_1)
ax_s_x.plot(time_series_1, label='Reference Signal (sin(t))', color='black', linewidth=2.)
ax_s_x.set_xlim([0, len(time_series_1) - 1])  # Set x-axis limit
ax_s_x.set_xlabel('Time')
ax_s_x.set_ylabel('Amplitude')

# Plotting the dependent signal (time_series_2)
ax_s_y.plot(-time_series_2, np.arange(len(time_series_2)), label='Dependent Signal (cos(t))', color='black', linewidth=2.)
ax_s_y.set_ylim([0, len(time_series_2) - 1])  # Set y-axis limit
ax_s_y.set_xlabel('Amplitude')
ax_s_y.set_ylabel('Time')

plt.tight_layout()
plt.show()
