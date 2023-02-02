import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import outlier.data as dataset
import outlier.config as CONF
import outlier.helper as helper
import seaborn as sns
import outlier.calc as calc
import tkinter as tk
from tkinter import scrolledtext

from matplotlib.backend_bases import MouseButton

from scipy import stats
from sklearn.neighbors import KernelDensity
import os
MAX_TEMPO = 200
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

def generateArtistsHeatMap(artists,x_discriminator="tempo",title=None):
    MAX_TEMPO = 50

    kde_map = np.zeros([len(artists),MAX_TEMPO])
    #artist_id = np.linspace(0, len(artists), num=len(artists))
    for i,artist in enumerate(artists):
        data = dataset.getDataFromArtist(artist)
        if not data : return print("无效的作曲家ID")
        x = np.array(list(map(lambda x: x[x_discriminator], data)))
        _, kde_y = calc.kde(x,n=MAX_TEMPO)
        kde_map[i,:] = kde_y

    # Draw
    df = pd.DataFrame(kde_map, index=artists)
    ax = sns.heatmap(df.transpose(),annot=False)
    ax.invert_yaxis()
    plt.title(title + " ("+str(len(artists))+")")
    plt.xlabel('Artist ID')
    plt.ylabel('Tempo')
    plt.show()
def generateArtistHeatMap(artist,x_discriminator="tempo"):
    MAX_TEMPO = 200

    kde_map = np.zeros([1,MAX_TEMPO])
    data = dataset.getDataFromArtist(artist)
    if not data : return print("无效的作曲家ID")
    x = np.array(list(map(lambda x: x[x_discriminator], data)))
    #y = np.array(list(map(lambda y: y[y_discriminator], data)))

    #coord = np.zeros([len(x),2])
    #for j in range(0,len(x)): coord[j] = [x[j],y[j]]

    _, kde_y = calc.kde(x,n=MAX_TEMPO)
    kde_map[0,:] = kde_y


    # Draw
    ax = sns.heatmap(kde_map.transpose(),annot=False)
    ax.invert_yaxis()
    plt.xlabel('Artist ID')
    plt.ylabel('Tempo')
    plt.show()
def generateAllArtistGraph(artists,x_discriminator="tempo",y_discriminator="loudness"):
    for i,artist in enumerate(artists):
        data = dataset.getDataFromArtist(artist)
        if not data : return print("无效的作曲家ID")
        x = np.array(list(map(lambda x: x[x_discriminator], data)))
        y = np.array(list(map(lambda y: y[y_discriminator], data)))

        plt.scatter(x,y)
    plt.show()
def generateAllArtistKdeGraph(artists,discriminator="tempo"):
    for i, artist in enumerate(artists):
        data = dataset.getDataFromArtist(artist)
        if not data: return print("无效的作曲家ID")
        x = dataset.getDataFromArtistByFeatureDiscriminator(artist,discriminator,filterNoise=True)
        #sns.kdeplot(x)
        print(x)
        x,y = calc.kde(x,n=MAX_TEMPO)
        plt.plot(x,y)

    plt.title("KDE - "+discriminator)
    plt.show()

def generateGenreHeatMap(genre,discriminator="tempo"):
    artists_list = dataset.getArtistsByGenre(genre)
    generateArtistsHeatMap(artists_list, x_discriminator=discriminator, title=genre.upper())

def generateInteractionPlotFromArtistList(artists,dx="tempo",dy="loudness"):
    fig, ax = plt.subplots(picker=True)
    for i, artist in enumerate(artists):
        # get song info
        data = dataset.getDataFromArtist(artist)
        x = dataset.getDataFromArtistByFeatureDiscriminator(artist,dx,filterNoise=False)
        y = dataset.getDataFromArtistByFeatureDiscriminator(artist,dy,filterNoise=False)
        plt.scatter(x,y,s=10)


    def onclick(event):
        print(event)
    cid = fig.canvas.mpl_connect("pick_event", onclick)
    plt.show()
