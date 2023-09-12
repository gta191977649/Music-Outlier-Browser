import os.path
import numpy as np
import vendor.hdf5.hdf5_getters as hdf5_getters
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

x_feature = "tempo"
y_feature = "loudness"

def getSectionFeatureFromSegments(song,segment_feature):
    section_starts = hdf5_getters.get_sections_start(song)
    segment_starts = hdf5_getters.get_segments_start(song)
    # segment_loudness = hdf5_getters.get_segments_loudness_max(song)


    section_feature = []

    for i in range(len(section_starts) - 1):
        start_time = section_starts[i]
        end_time = section_starts[i + 1]
        #print(start_time, end_time)
        # Identify segments within this section
        segments_in_section = np.array([feature for start, feature in zip(segment_starts, segment_feature) if start_time <= start < end_time])

        # Aggregate loudness
        if segments_in_section.any():
            aggregated_feature = np.mean(segments_in_section)
        else:
            aggregated_feature = np.nan  # or some other placeholder value

        section_feature.append(aggregated_feature)
    return section_feature
def getSectionFeature(song, feature='loudness'):
    if feature == "loudness":
        segment_feature = hdf5_getters.get_segments_loudness_max(song)
        return getSectionFeatureFromSegments(song,segment_feature)
    if feature == "mfcc":
        segment_feature = hdf5_getters.get_segments_timbre(song)
        return getSectionFeatureFromSegments(song,segment_feature)
    if feature == "pitch":
        segment_feature = hdf5_getters.get_segments_pitches(song)
        return getSectionFeatureFromSegments(song,segment_feature)
    if feature == "tempo":
        tempo = hdf5_getters.get_tempo(song)
        num_segments = len(hdf5_getters.get_sections_start(song))-1
        return np.full(num_segments, tempo)

if __name__ == '__main__':
    ARTIST_NAME = "blue_oyster_cult"
    f = open("{}.txt".format(ARTIST_NAME))
    #f = open("artist_list_one.txt")
    lines = f.readlines()

    data = []
    all_x = []
    all_y = []

    plt.figure(figsize=(6, 8))
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax0 = plt.subplot(gs[0])

    for song in lines:
        ID = song.strip()
        #if os.path.exists("../data/MSD/" + ID + ".h5"):
        if os.path.exists("../data/{}/{}.h5".format(ARTIST_NAME,ID)):
            song = hdf5_getters.open_h5_file_read("../data/{}/{}.h5".format(ARTIST_NAME,ID))
            sr = hdf5_getters.get_analysis_sample_rate(song)
            x = getSectionFeature(song, feature=x_feature)
            y = getSectionFeature(song, feature=y_feature)
            title = hdf5_getters.get_title(song)
            #print(title)
            all_x.extend(x)
            all_y.extend(y)
            sns.scatterplot(x=x, y=y, ax=ax0)

    ax0.set_title('{} - Section Feature Plot'.format(ARTIST_NAME))
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
