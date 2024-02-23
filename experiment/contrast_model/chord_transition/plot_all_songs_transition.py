from PlotChordTransition import *
import os
import pandas as pd
from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import matplotlib.pyplot as plt
from chordify import feature_extractor as feature
import ast

if __name__ == '__main__':
    # transistChart = PlotChordTransition()
    #
    # # Add major and minor transitions as needed
    # transistChart.addChordTransition("Amaj", "Fmin")
    # transistChart.addChordTransition("Cmin", "Gmin")
    #
    # # Show the plot with transitions
    # transistChart.showPlot()

    MODE = "minor"
    TRANSPOSED = True
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/abba"
    meta_path = os.path.join(BASE_PATH, "meta.csv")
    files = pd.read_csv(meta_path)

    chords_ls = []
    song_name_ls = []
    frequency_ls = []
    transistChart = PlotChordTransition(mode=MODE,title=f"Transition Chart\n{BASE_PATH} {MODE}")
    for _, song in files.iterrows():
        if not song["mode"] == MODE: continue
        title = song["title"]
        #filename = title.replace(".mp3", "_transposed.lab" if TRANSPOSED else ".lab")
        filename = title.replace(".mp3",".csv")
        pattern_path = os.path.join(BASE_PATH, "pattern", filename)
        if os.path.exists(pattern_path):
            data = pd.read_csv(pattern_path)
            for _,pattern in data.iterrows():
                transitions = ast.literal_eval(pattern["transitions"])
                frequency = pattern["frequency"]
                #add * times for matched patterns
                for _ in range(frequency):
                    for i in range(len(transitions)):
                        if not transitions[i - 1]: continue
                        transistChart.addChordTransition(transitions[i - 1], transitions[i])
    transistChart.showPlot()


    # transistChart = PlotChordTransition(mode=MODE)
    # current_chord = None
    # for i in range(len(chords_ls)):
    #     if not chords_ls[i - 1]: continue
    #     if not chords_ls[i] == current_chord:
    #         current_chord = chords_ls[i]
    #         transistChart.addChordTransition(chords_ls[i - 1], chords_ls[i])
    #
    # transistChart.showPlot()
