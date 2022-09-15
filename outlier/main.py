from outlier import Outlier
import data as dataset
import helper as helper
import numpy as np
import result as output
# Do outlier detection for each artist
def doOutlierDetection():
    artist_list = dataset.getAllArtistList()
    for artist in artist_list:
        outliers = outlier.artist(artist,x_discriminator="tempo",y_discriminator="loudness")
        print(artist)
        print(outliers)

def doOutlierGraphGeneration(n,random=False):
    #artists = dataset.getAllArtistList(min=10)
    artists = ["Blue Oyster Cult"]
    #artists = np.random.choice(artists, n, replace=False) if random else artists[0:n]
    #outlier.generateArtistGraph(artists)
    output.generateArtistHeatMap(artists)

if __name__ == '__main__':
    outlier = Outlier()
    #outliers = outlier.artist("Blue Oyster Cult",x_discriminator="tempo",y_discriminator="loudness")
    #artists = ["Blue Oyster Cult", "Cyndi Lauper", "Frankie Valli"]
    doOutlierGraphGeneration(100,True)
    