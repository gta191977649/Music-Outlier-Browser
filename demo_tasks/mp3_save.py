from youtubesearchpython import VideosSearch
import yt_dlp
import vendor.hdf5.hdf5_getters as hdf5_getters
import os
def search_youtube(query, limit=1):
    search = VideosSearch(query, limit=limit)
    result = search.result()
    if result and result['result']:
        return result['result'][0]['link']
    else:
        return None

def download_audio_from_youtube(link,name="test", output_folder='./music'):
    """
    Download audio from a given YouTube link.
    Parameters:
    - link: YouTube video link.
    - output_folder: Folder to save the downloaded audio. By default, the current directory.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/vendor/ffmpeg',  # Replace with the actual path
        'outtmpl': "{}/{}".format(output_folder,name),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

if __name__ == '__main__':

    # song_name = input("Enter the name of the song: ")
    # video_link = search_youtube(song_name)
    # print(f"Video link: {video_link}")
    # download_audio_from_youtube(video_link)

    ARTIST_NAME = "blue_oyster_cult"
    f = open("{}.txt".format(ARTIST_NAME))
    lines = f.readlines()

    for song in lines:
        ID = song.strip()
        # if os.path.exists("../data/MSD/" + ID + ".h5"):
        if os.path.exists("../data/{}/{}.h5".format(ARTIST_NAME, ID)):
            song = hdf5_getters.open_h5_file_read("../data/{}/{}.h5".format(ARTIST_NAME, ID))
            title = hdf5_getters.get_title(song)
            artist = hdf5_getters.get_artist_name(song)
            print(title)
            video_link = search_youtube("{} - {}".format(title,artist))
            download_audio_from_youtube(video_link, output_folder='../music/{}'.format(artist),name=ID)
