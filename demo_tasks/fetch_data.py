import os.path
from pytube import YouTube
from youtubesearchpython import VideosSearch
import vendor.hdf5.hdf5_getters as hdf5_getters

if __name__ == '__main__':
    f = open("artilst_datalist.txt")
    lines = f.readlines()
    for song in lines:
        ID = song.strip()
        if os.path.exists("../data/MSD/"+ID+".h5"):
            song = hdf5_getters.open_h5_file_read("../data/MSD/"+ID+".h5")
            title = hdf5_getters.get_title(song)
            artist = hdf5_getters.get_artist_name(song)
            sections = hdf5_getters.get_segments_timbre(song)
            print(title,artist)
            print(sections)


    # song = hdf5_getters.open_h5_file_read("../data/MSD/"+songs[0]+".h5")
    # #section_data = hdf5_getters.get_segments_loudness_max(song)
    # section_data = hdf5_getters.get_sections_start(song)
    # title = hdf5_getters.get_title(song)
    # artist = hdf5_getters.get_artist_name(song)
    # print(section_data,artist,title)
