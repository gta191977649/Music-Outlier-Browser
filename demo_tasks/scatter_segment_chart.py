import vendor.hdf5.hdf5_getters as hdf5_getters
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

songs = [
    "TRAMTGD128F4260B66",
]


if __name__ == '__main__':
    song = hdf5_getters.open_h5_file_read("../dataset/MSD/"+songs[0]+".h5")
    #section_data = hdf5_getters.get_segments_loudness_max(song)
    section_data = hdf5_getters.get_sections_start(song)
    print(section_data)


