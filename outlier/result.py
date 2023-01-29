import matplotlib.pyplot as plt
import numpy as np
import outlier.data as dataset
import outlier.config as CONF
import outlier.helper as helper
import seaborn as sns
import outlier.calc as calc
from scipy import stats

import os

def generateArtistGraph(artists,x_discriminator="tempo",y_discriminator="loudness"):
    for artist in artists:
        data = dataset.getDataFromArtist(artist)
        x = np.array(list(map(lambda x: x[x_discriminator], data)))
        y = np.array(list(map(lambda y: y[y_discriminator], data)))
        plt.scatter(x,y)
        path = CONF.WORK_DIR+helper.escapePath(artist)+".png"
        print(path)
        plt.title(artist)
        plt.savefig(path)
        plt.close()
def generateArtistHeatMap(artists,x_discriminator="tempo",y_discriminator="loudness"):
    for artist in artists:
        print(artist)
        data = dataset.getDataFromArtist(artist)
        x = np.array(list(map(lambda x: x[x_discriminator], data)))
        y = np.array(list(map(lambda y: y[y_discriminator], data)))
        # Draw
        #sns.displot(x=x, kind="kde")
        g = sns.kdeplot(x=x,y=y,bw_adjust=0.4,levels=1)
        data = []
        for i in g.get_children():
            print(i.__class__.__name__)
            if i.__class__.__name__ == 'PathCollection':
                data.append(i.get_paths())

        print(data[0])

        plt.scatter(x, y)
        path = CONF.WORK_DIR + helper.escapePath(artist) + "_heatmap.png"
        print(path)
        plt.title(artist)
        plt.savefig(path)
        plt.close()

def generateAllGraph(artists,x_discriminator="tempo"):
    tempo_max = 200
    #tempo = np.linspace(0, 200, num=tempo_max)
    kde_map = np.zeros([len(artists),tempo_max])
    #artist_id = np.linspace(0, len(artists), num=len(artists))
    for i,artist in enumerate(artists):
        data = dataset.getDataFromArtist(artist)
        if not data : return print("无效的作曲家ID")
        x = np.array(list(map(lambda x: x[x_discriminator], data)))
        _, kde_y = calc.kde(x,n=tempo_max)
        kde_map[i,:] = kde_y


    # Draw
    ax = sns.heatmap(kde_map.transpose(),annot=False)
    ax.invert_yaxis()
    plt.xlabel('Artist ID')
    plt.ylabel('Tempo')
    plt.show()

    artist_id = 5
    #buffer.append([x_mean])



    # Draw
    #data = np.array([x,y])
    #print(data)
    #sns.heatmap(buffer,annot=True)
    #data = []
    #plt.show()
