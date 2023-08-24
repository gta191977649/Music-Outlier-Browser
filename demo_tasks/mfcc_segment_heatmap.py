import vendor.hdf5.hdf5_getters as hdf5_getters
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

songs = [
    "TRAJTCL128F1460CDA.h5",
    "TRAAAMQ128F1460CD3.h5"
]


def plot_mfcc_heatmap(song_path, song_name, ax):
    song = hdf5_getters.open_h5_file_read(song_path)
    section_mfccs = hdf5_getters.get_segments_timbre(song)

    sns.heatmap(section_mfccs.T, ax=ax, cmap='viridis', cbar=True)
    ax.set_title(f"MFCC Heatmap for {song_name}")
    ax.set_xlabel("Segments")
    ax.set_ylabel("MFCC Coefficients")


if __name__ == '__main__':
    fig, axs = plt.subplots(len(songs), 1, figsize=(12, 8 * len(songs)))

    for idx, song_file in enumerate(songs):
        song_name = song_file.split(".")[0]
        plot_mfcc_heatmap(f"../dataset/file/{song_file}", song_name, axs[idx])

    plt.tight_layout()
    plt.show()
