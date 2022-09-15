import matplotlib.pyplot as plt
import numpy as np
import data as dataset
import config as CONF
import helper as helper
import seaborn as sns

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

