import vendor.hdf5.hdf5_getters as hdf5_getters
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

songs = [
    "TRAJTCL128F1460CDA.h5",
    "TRAAAMQ128F1460CD3.h5"
]


def plot_mfcc_density(song_path, song_name, ax1, ax2):
    song = hdf5_getters.open_h5_file_read(song_path)
    section_data = hdf5_getters.get_segments_timbre(song)
    #section_data = hdf5_getters.get_segments_pitches(song)

    # Plotting individual MFCC segments on the first subplot
    for i in range(section_data.shape[1]):
        sns.kdeplot(section_data[:, i], ax=ax1, label=f"Segment {i + 1} MFCC of {song_name}")

    # Plotting flattened MFCCs for the entire song on the second subplot
    sns.kdeplot(section_data.flatten(), ax=ax2, label=f"Flattened MFCCs of {song_name}")


if __name__ == '__main__':
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))

    for song_file in songs:
        song_name = song_file.split(".")[0]
        plot_mfcc_density(f"../dataset/file/{song_file}", song_name, ax1, ax2)

    ax1.set_title("Density Diagram of Individual MFCC Segments for Songs")
    ax1.set_xlabel("MFCC Value")
    ax1.set_ylabel("Density")
    ax1.legend()

    ax2.set_title("Density Diagram of Flattened MFCCs for Songs")
    ax2.set_xlabel("MFCC Value")
    ax2.set_ylabel("Density")
    ax2.legend()

    plt.tight_layout()
    plt.show()
