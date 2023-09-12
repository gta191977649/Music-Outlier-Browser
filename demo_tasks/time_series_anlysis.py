import os.path
import numpy as np
import vendor.hdf5.hdf5_getters as hdf5_getters
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

x_feature = "loudness"
SMOOTH = False  # Set this to True to enable smoothing, and False to disable
WINDOW_SIZE = 20  # Size of the smoothing window

def getSongFeature(song, feature='loudness'):
    if feature == "loudness":
        return hdf5_getters.get_segments_loudness_max(song)
    if feature == "mfcc":
        return np.mean(hdf5_getters.get_segments_timbre(song), axis=1)
    if feature == "pitch":
        return np.mean(hdf5_getters.get_segments_pitches(song), axis=1)
    if feature == "tempo":
        tempo = hdf5_getters.get_tempo(song)
        num_segments = len(hdf5_getters.get_segments_start(song))
        return np.full(num_segments, tempo)
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

if __name__ == '__main__':
    ARTIST_NAME = "blue_oyster_cult"
    f = open("{}.txt".format(ARTIST_NAME))
    lines = f.readlines()

    all_features = []  # To collect all segment features across all songs

    plt.figure(figsize=(8, 10))

    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    # First subplot for time-series
    ax0.set_xlabel('Time (seconds)')
    ax0.set_ylabel('Loudness')
    ax0.set_title('Time-series of Loudness Across Song Segments')
    ax0.grid(True)

    for idx, song in enumerate(lines):
        ID = song.strip()
        if os.path.exists("../data/{}/{}.h5".format(ARTIST_NAME, ID)):
            song = hdf5_getters.open_h5_file_read("../data/{}/{}.h5".format(ARTIST_NAME, ID))
            x = getSongFeature(song, feature=x_feature)
            all_features.extend(x)  # Add to the collection
            title = hdf5_getters.get_title(song).decode('utf-8')

            if SMOOTH:
                x_smooth = moving_average(x, WINDOW_SIZE)
                ax0.plot(range(len(x_smooth)), x_smooth, marker='o', linestyle='-', label=f"{title} (Song {idx + 1})")
            else:
                ax0.plot(range(len(x)), x, marker='o', linestyle='-', label=f"{title} (Song {idx + 1})")

    # Second subplot for density
    ax1.set_xlabel(x_feature)
    ax1.set_ylabel('Count')
    ax1.set_title('Density of {} Across All Segments'.format(x_feature))
    ax1.hist(all_features, bins=50, edgecolor='black')
    #ax1.grid(True)

    plt.tight_layout()
    plt.show()