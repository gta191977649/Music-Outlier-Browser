# This file is test each module functionaities,
# it's not the testing framework to envaluate the model performance.
import time
from song import Song
from player import Player
import os.path
import plot as plot

def plotAllContrastPlotForAritst(artistname):
    ARTIST_NAME = artistname
    for idx, filename in enumerate(os.listdir("../data/{}/".format(ARTIST_NAME))):
        full_file_path = os.path.join("../data/{}/".format(ARTIST_NAME), filename)
        song = Song(full_file_path, feature="loudness")
        song.plot(showLegend=False)
        start_1, end_1, start_2, end_2 = song.getHighestContrastSectionTime()
        print("Highest Contrast Section: [{}-{}] to [{}-{}]".format(start_1, end_1, start_2, end_2))
        time.sleep(1)

if __name__ == '__main__':
    path = "../music/bokunanka.wav"
    #path = "../data/blue_oyster_cult/TRASNUX128F425EAF2.h5"
    song = Song(path, feature="mfcc",filterBank="mel")
    s = song.section_features
    print(s)
    plot.plot_signals_by_sections(song.section_features, title=path)
    #plot.plot_chroma_by_sections(song.section_features, title=path)
    # player = Player(song)
    # player.show()
    # # song.plot(showLegend=False)
    # start_1, end_1, start_2, end_2 = song.getHighestContrastSectionTime()
    # print("Highest Contrast Section: [{}-{}] to [{}-{}]".format(start_1, end_1, start_2, end_2))
    # #song.plotSectionDTW()