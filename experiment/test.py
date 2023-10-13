# This file is test each module functionaities,
# it's not the testing framework to envaluate the model performance.
import time
from song import Song
import os.path
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
    #song = Song("../data/colin_meloy/TRQYFYM128F4272098.h5", feature="loudness")
    song = Song("../music/bokunanka.wav", feature="loudness")
    song.plot(showLegend=False)
    start_1, end_1, start_2, end_2 = song.getHighestContrastSectionTime()
    print("Highest Contrast Section: [{}-{}] to [{}-{}]".format(start_1, end_1, start_2, end_2))
    song.plotSectionDTW()