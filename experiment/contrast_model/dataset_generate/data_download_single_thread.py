import h5py
import pandas as pd
import numpy as np
import yt_dlp as dl
import os

def create_dataset(dataset_name):
    # Create a new HDF5 file
    with h5py.File('/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/example.h5', 'w') as f:
        # Create a dataset in the file

        gp_chord = f.create_group("chord")
        gp_chord.create_dataset("a", data=[1,2,3])

        dataset = f.create_dataset("b", data=["A","B","C"])

        # Optionally, you can specify dataset properties such as compression
        # compressed_dataset = f.create_dataset("CompressedData", data=data, compression="gzip")

    print("Dataset created successfully.")

def search_download_song(search_term,location):
    dl_opts = {
        'audio-format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                'preferredcodec': 'mp3',  # Specify audio format to mp3
                'preferredquality': '100',  # Specify audio quality
            },

        ],
        'postprocessor_args': [
            #'-ar', '16000',
            '-ac', '1'  # convert to mono
        ],
        'outtmpl': location, #save to path
    }

    # Initialize YoutubeDL with the options
    with dl.YoutubeDL(dl_opts) as ydl:
        ydl.download([f'ytsearch1:{search_term}'])

if __name__ == '__main__':
    SIZE = 10000 # get first 10000 data
    BASE_PATH = '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all'
    track_file_path = os.path.join(BASE_PATH, "track.txt")
    meta_data = pd.read_csv("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/id_information.csv",delimiter="\t")
    meta_data = meta_data.sort_values(by='artist')
    meta_data = meta_data[:5]
    print(meta_data)

    #search_download_song("Bic Camera Theme Song","/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/")
    for _,song in meta_data.iterrows():
        title = song['song']
        artist = song['artist'].lower().strip()
        album_name = song['album_name']
        id = song["id"]
        DOWNLOAD_PATH = os.path.join(BASE_PATH,artist,f"{id}")
        if os.path.exists(DOWNLOAD_PATH+".mp3"):
            print(f"☑️Skipping already downloaded song: {song['song']} - {song['artist']} ({id})")
            continue

        print(f"⏬Downloading song: {title} - {artist} ({id})")
        SEARCH_TERM = f"{title} - {album_name}"
        search_download_song(SEARCH_TERM,
                             DOWNLOAD_PATH)



