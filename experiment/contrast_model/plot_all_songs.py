import os
import pandas as pd
from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import matplotlib.pyplot as plt

def map_music21(chord_21,name):
    map_21 = {'A': eNote.A,
              'D': eNote.D,
              'G': eNote.G,
              'C': eNote.C,
              'F': eNote.F,
              'Bb': eNote.Bb,
              'A#': eNote.Bb,
              'Eb': eNote.Eb,
              'D#': eNote.Eb,
              'G#': eNote.Ab,
              'Ab': eNote.Ab,
              'C#': eNote.Db,
              'Db': eNote.Db,
              'F#': eNote.Fsharp,
              'Gb': eNote.Fsharp,
              'B': eNote.B,
              'E': eNote.E}
    temp = []
    for i in chord_21:
        temp.append(map_21[i])

    return VectorModel(temp,name=name)

def getChordVectorsFromFile(PATH_CHORD):
    chords = []
    with open(PATH_CHORD, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Skip the line if it starts with '#'
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) == 3:
                start, end, chord_str = parts
                # SKIP NONE CHORD
                if chord_str in ["N", "None"]: continue
                chord_str = chord_str.replace(":","")
                c = Chord(chord_str)
                notes = c.components()
                v = map_music21(notes, chord_str)
                chords.append({
                    "chord":v,
                    "angle":v.temp_theta,
                    "beat":end,
                })
    return chords

if __name__ == '__main__':
    print("Plot all songs")
    MODE = "minor"
    TRANSPOSED = True


    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/abba"
    meta_path = os.path.join(BASE_PATH,"meta.csv")
    files = pd.read_csv(meta_path)

    vector_ls = []
    song_name_ls = []
    for _,song in files.iterrows():
        if not song["mode"] == MODE: continue
        title = song["title"]
        filename = title.replace(".mp3", "_transposed.lab" if TRANSPOSED else ".lab")
        chord_path = os.path.join(BASE_PATH,"chord",filename)
        if os.path.exists(chord_path):
            chords = getChordVectorsFromFile(chord_path)
            song_vevtor = []
            for item in chords:
                song_vevtor.append(item["angle"])
            vector_ls.append(song_vevtor)
            song_name_ls.append(title)
    print(vector_ls)

    plt.figure(figsize=(30, 5))  # Set the figure size as needed
    for i, song_vector in enumerate(vector_ls):
        # Generate x values based on the length of the song_vector
        x = range(len(song_vector))

        # Plot each song's vector angles
        #plt.step(x, song_vector, where='mid', label=f'Song {i + 1}')
        plt.plot(x, song_vector, label=f'Song {song_name_ls[i]}')

    plt.xlabel('Time')
    plt.ylabel('Chord Angle')
    plt.title('Chord Angle Progression for Each Song')
    plt.legend()  # Add a legend to distinguish between songs
    plt.show()