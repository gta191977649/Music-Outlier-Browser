import vendor.hdf5.hdf5_getters as hdf5_getters
import numpy as np
if __name__ == '__main__':
    song = hdf5_getters.open_h5_file_read("../data/MSD/TRSIZRN128F427DB95.h5")
    section_starts = hdf5_getters.get_sections_start(song)
    segment_starts = hdf5_getters.get_segments_start(song)
    #segment_loudness = hdf5_getters.get_segments_loudness_max(song)
    segment_feature = np.mean(hdf5_getters.get_segments_timbre(song),axis=1)

    section_loudness = []

    for i in range(len(section_starts) - 1):
        start_time = section_starts[i]
        end_time = section_starts[i + 1]
        print(start_time,end_time)
        # Identify segments within this section
        segments_in_section = [feature for start, feature in zip(segment_starts, segment_feature) if
                               start_time <= start < end_time]

        # Aggregate loudness
        if segments_in_section:
            aggregated_feature = np.mean(segments_in_section)
        else:
            aggregated_feature = np.nan  # or some other placeholder value

        section_loudness.append(aggregated_feature)
    print(section_loudness)
