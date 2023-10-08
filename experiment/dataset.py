import numpy as np
import vendor.hdf5.hdf5_getters as hdf5_getters
def summarySection(segments_in_section,method="mean"):
    if method == "mean":
        return np.mean(segments_in_section)
    if method == "median":
        return np.median(segments_in_section)
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
    if method == "percentile_25":
        return np.percentile(segments_in_section, 25)
    if method == "percentile_75":
        return np.percentile(segments_in_section, 75)
    if method == "rms":
        return np.sqrt(np.mean(np.square(segments_in_section)))

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

        section_feature.append({
            "time":[start_time,end_time],
            "feature":segments_in_section,
        })
    return section_feature
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

    return section_feature

def getData(full_file_path):
    return hdf5_getters.open_h5_file_read(full_file_path)

