import os.path
import numpy as np
import vendor.hdf5.hdf5_getters as hdf5_getters
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

x_feature = "tempo"
y_feature = "loudness"


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


if __name__ == '__main__':
    ARTIST_NAME = "blue_oyster_cult"
    f = open("{}.txt".format(ARTIST_NAME))
    lines = f.readlines()
    data = []
    all_x = []
    all_y = []

    plt.figure(figsize=(6, 8))

    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])

    # Scatter plot
    ax0 = plt.subplot(gs[0])
    for song in lines:
        ID = song.strip()
        # if os.path.exists("../data/MSD/" + ID + ".h5"):
        if os.path.exists("../data/{}/{}.h5".format(ARTIST_NAME, ID)):
            song = hdf5_getters.open_h5_file_read("../data/{}/{}.h5".format(ARTIST_NAME, ID))
            title = hdf5_getters.get_title(song)
            artist = hdf5_getters.get_artist_name(song)
            x = getSongFeature(song, feature=x_feature)
            y = getSongFeature(song, feature=y_feature)
            all_x.extend(x)
            all_y.extend(y)
            sns.scatterplot(x=x, y=y, ax=ax0)

    ax0.set_title('{} - Segment Feature Plot'.format(ARTIST_NAME))
    ax0.set_xlabel(x_feature)
    ax0.set_ylabel(y_feature)

    # Histogram for x_feature
    ax1 = plt.subplot(gs[1])
    sns.histplot(all_x, bins=50, kde=True, ax=ax1)
    ax1.set_title(f'Density of {x_feature}')
    ax1.set_xlabel(x_feature)
    ax1.set_ylabel('Frequency')

    # Histogram for y_feature
    ax2 = plt.subplot(gs[2])
    sns.histplot(all_y, bins=50, kde=True, ax=ax2)
    ax2.set_title(f'Density of {y_feature}')
    ax2.set_xlabel(y_feature)
    ax2.set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()
