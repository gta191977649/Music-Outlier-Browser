import pandas as pd

import outlier.outlier as OutlierDetection
import outlier.data as dataset
import outlier.helper as helper
import outlier.result as result
import numpy as np
import outlier.result as output
import pandas as pd
import outlier.config as CONF
from tqdm import tqdm
import seaborn as sns

# Do outlier detection for each artist
def doOutlierDetection():
    artist_list = dataset.getAllArtistList()
    for artist in artist_list:
        outliers = outlier.artist(artist,x_discriminator="tempo",y_discriminator="loudness")
        print(artist)
        print(outliers)

def doOutlierGraphGeneration(n,random=False):
    # artists = ["Blue Oyster Cult"]
    # artists = np.random.choice(artists, n, replace=False) if random else artists[0:n]
    # outlier = OutlierDetection.Outlier()

    artists = dataset.getAllArtistList(min=10)
    result.generateArtistHeatMap(artists)
    # print(artists)
    #output.generateArtistHeatMap(artists)
    #doOutlierDetection()

def generateOutlierDetection():
    output = []
    outlier = OutlierDetection.Outlier()
    artist_list = dataset.getAllArtistList()
    artist_list = artist_list
    for artist in tqdm(artist_list):
        # get outliers list from artist (if any)
        outliers = outlier.artist(artist)
        songs = dataset.getDataFromArtist(artist)
        for song in songs:
            frame = {}
            frame["id"] = song["id"]
            frame["artist"] = song["artist"]
            frame["name"] = song["title"]
            frame["link"] = ""
            frame["algo_outlier"] = 0
            frame["outlier_class"] = ""
            if song["id"] in outliers:
                frame["algo_outlier"] = 1
                output.append(frame)

    # convert to pandas
    output = pd.DataFrame(output)
    output.to_csv(CONF.CSV_DIR+"outliers.csv",index=False)
    print(output)

if __name__ == '__main__':
    #print(np.random.rand(10, 10))
    outlier = OutlierDetection.Outlier()
    #data = dataset.getDataFromArtist("Deadmau5")
    #generateOutlierDetection()


    #print(artist_list)
    #result.generateAllGraph(artist_list)
    #result.generateAllArtistGraph(["MNEMIC"])
    #result.generateArtistsHeatMap(['Deadmau5','Benga','Blue Six','Bug'z In The Attic'],x_discriminator="tempo",title="Dance & Electronica")
    #result.generateGenreHeatMap("hip-hop", discriminator="loudness")
    # artist_list = dataset.getAllArtistList(min=10)[:10]



    artist_list = [
        "Blue Oyster Cult",
        #"MNEMIC",
        "Colin Meloy",
        #"Rod Lee"
    ]
    #result.generateInteractionPlotFromArtistList(artist_list)
