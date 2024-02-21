from PlotChordTransition import *
import os
import pandas as pd
from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import matplotlib.pyplot as plt
from chordify import feature_extractor as feature

if __name__ == '__main__':
    # transistChart = PlotChordTransition()
    #
    # # Add major and minor transitions as needed
    # transistChart.addChordTransition("Amaj", "Fmin")
    # transistChart.addChordTransition("Cmin", "Gmin")
    #
    # # Show the plot with transitions
    # transistChart.showPlot()

    MODE = "major"
    TRANSPOSED = True
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/abba"
    meta_path = os.path.join(BASE_PATH, "meta.csv")
    files = pd.read_csv(meta_path)

    chords_ls = []
    song_name_ls = []
    for _, song in files.iterrows():
        if not song["mode"] == MODE: continue
        title = song["title"]
        filename = title.replace(".mp3", "_transposed.lab" if TRANSPOSED else ".lab")
        chord_path = os.path.join(BASE_PATH, "chord", filename)
        if os.path.exists(chord_path):
            chords = feature.getChordVectorsFromFile(chord_path)
            for chord in chords:
                if not chord["name"] == None:
                    chords_ls.append(chord["name"])

    transistChart = PlotChordTransition(mode=MODE)
    current_chord = None
    for i in range(len(chords_ls)):
        if not chords_ls[i - 1]: continue
        if not chords_ls[i] == current_chord:
            current_chord = chords_ls[i]
            transistChart.addChordTransition(chords_ls[i - 1], chords_ls[i])

    transistChart.showPlot()
