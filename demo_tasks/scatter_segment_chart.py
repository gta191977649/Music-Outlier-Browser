import vendor.hdf5.hdf5_getters as hdf5_getters
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

songs = [
    "TRAJTCL128F1460CDA.h5",
    "TRAAAMQ128F1460CD3.h5"
]


if __name__ == '__main__':
    song = hdf5_getters.open_h5_file_read(f"../dataset/file/{songs[0]}")
    section_data = hdf5_getters.get_segments_loudness_max(song)
    #section_data = hdf5_getters.get_segments_pitches(song)


    sns.lineplot(section_data)
    plt.show()
