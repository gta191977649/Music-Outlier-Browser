# This file is test each modules functionaities,
# it's not the testing framework to envaluate the model performance.
from song import Song

if __name__ == '__main__':
    song = Song("../data/deadmu5/TRAHTFN128F9330150.h5",feature="loudness")
    song.plot()