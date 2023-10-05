import os.path
import numpy as np
import vendor.hdf5.hdf5_getters as hdf5_getters
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from scipy import stats
from tslearn.metrics import dtw_path

x_feature = "loudness"
summary_method = "mean"
NORMALIZED = False
ARTIST_NAME = "deadmu5"


def section_difference(section_features):
    """
    Calculate the difference between the mean values of adjacent sections.
    """
    differences = []
    differences = [(section_features[i+1] - section_features[i]) for i in range(len(section_features) - 1)]
    # for i in range(len(section_features) - 1):
    #     path,sim = dtw_path(section_features[i+1], section_features[i])
    #     differences.append(sim)
    #return np.abs(differences)
    return differences

def summarySection(segments_in_section,method="mean"):
    if method == "mean":
        return np.mean(segments_in_section)
    if method == "median":
        return np.median(segments_in_section)
    if method == "mode":
        return stats.mode(segments_in_section)[0][0]
    if method == "std":
        return np.std(segments_in_section)
    if method == "variance":
        return np.var(segments_in_section)
    if method == "range":
        return np.ptp(segments_in_section)
    if method == "min":
        return np.min(segments_in_section)
    if method == "max":
        return np.max(segments_in_section)
    if method == "sum":
        return np.sum(segments_in_section)
    if method == "skewness":
        return stats.skew(segments_in_section)
    if method == "kurtosis":
        return stats.kurtosis(segments_in_section)
    if method == "percentile_25":
        return np.percentile(segments_in_section, 25)
    if method == "percentile_75":
        return np.percentile(segments_in_section, 75)
    if method == "z_score":
        z_scores = stats.zscore(segments_in_section)
        return np.mean(z_scores)
    if method == "rms":
        return np.sqrt(np.mean(np.square(segments_in_section)))
    if method == "geometric_mean":
        return stats.gmean(segments_in_section)
    if method == "harmonic_mean":
        return stats.hmean(segments_in_section)
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
            aggregated_feature = summarySection(segments_in_section,method=summary_method)
        else:
            aggregated_feature = np.nan  # or some other placeholder value

        section_feature.append(aggregated_feature)
    return section_feature
def normalize_data(data):
    data_min = np.min(data)
    data_max = np.max(data)
    return 2 * ((data - data_min) / (data_max - data_min)) - 1

def getSectionFeature(song, feature='loudness'):
    global NORMALIZED  # Use the global flag

    if feature == "loudness":
        segment_feature = hdf5_getters.get_segments_loudness_max(song)
    elif feature == "mfcc":
        segment_feature = hdf5_getters.get_segments_timbre(song)
    elif feature == "pitch":
        segment_feature = hdf5_getters.get_segments_pitches(song)
    elif feature == "tempo":
        tempo = hdf5_getters.get_tempo(song)
        num_segments = len(hdf5_getters.get_sections_start(song)) - 1
        segment_feature = np.full(num_segments, tempo)

    section_feature = getSectionFeatureFromSegments(song, segment_feature)

    if NORMALIZED:
        section_feature = normalize_data(np.array(section_feature))

    return section_feature
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

all_features = []
if __name__ == '__main__':


    plt.figure(figsize=(8, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    # First subplot for time-series
    ax0.set_xlabel('Section Index')
    ax0.set_ylabel(x_feature)
    ax0.set_title('Time-series of {} Changes (Difference) Across Song Sections\n{}'.format(x_feature,ARTIST_NAME))
    ax0.grid(True)

    for idx, filename in enumerate(os.listdir("../data/{}/".format(ARTIST_NAME))):
        full_file_path = os.path.join("../data/{}/".format(ARTIST_NAME), filename)
        if os.path.exists(full_file_path):
            song = hdf5_getters.open_h5_file_read(full_file_path)
            x = getSectionFeature(song, feature=x_feature)
            x = section_difference(x)
            all_features.extend(x)  # Add to the collection
            title = hdf5_getters.get_title(song).decode('utf-8')

            ax0.plot(range(len(x)), x, marker='o', linestyle='-', label=f"{title} (Song {idx + 1})")
            #ax0.bar(range(len(x)), x, label=f"{title} (Song {idx + 1})")

    # Second subplot for density
    ax1.set_xlabel(x_feature)
    ax1.set_ylabel('Count')
    ax1.set_title('Density of {} Changes Across All Sections'.format(x_feature))
    ax1.hist(all_features, bins=50, edgecolor='black')
    ax1.grid(True)

    plt.tight_layout()
    plt.show()
df = pd.DataFrame(all_features)
df.to_csv("feature.csv")

