import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import outlier.outlier as OutlierDetection
import outlier.data as dataset
import outlier.helper as helper
import outlier.result as result
from sklearn.mixture import GaussianMixture
import numpy as np
import outlier.result as output
import pandas as pd
import outlier.config as CONF
from tqdm import tqdm
import seaborn as sns
from matplotlib.colors import ListedColormap
import mpltex
import csv

def graphLabel(clusters,dx="tempo",dy="loudness"):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink']
    for item in clusters["data"]:
        x = item[dx]
        y = item[dy]
        label = item["label"]
        plt.scatter(x=x,y=y,c=colors[label])
    plt.show()

def graphOutlier(clusters,dx="tempo",dy="loudness"):
    mpl.rcParams['font.family'] = 'Times New Roman'
    mpl.rcParams['font.size'] = 12
    colors = ['blue',  'orange','green', 'purple', 'yellow', 'pink']
    labels = []
    artist = clusters["data"][0]["artist"]
    for item in clusters["data"]:
        label = item["label"]
        labels.append(label)

    unique, counts = np.unique(labels, return_counts=True)
    occurrences = dict(zip(unique, counts))
    outlier_label = min(occurrences, key=lambda x: occurrences[x])
    print("label {} cluster is outlier".format(outlier_label))
    # draw graph with outlier
    data = []
    outliers = []
    for item in clusters["data"]:
        x = item[dx]
        y = item[dy]
        label = item["label"]
        data.append([x,y])
        #plt.scatter(x=x,y=y,color=colors)

        if label == outlier_label:
            outliers.append([x,y])
    data = np.array(data)
    outliers = np.array(outliers)

    plt.scatter(x=data[:,0],y=data[:,1], color="blue")
    plt.scatter(x=outliers[:,0],y=outliers[:,1],marker='x',color="red",s=100,label="Outlier")

    plt.legend()
    plt.title("Outliers: {} (k={})".format(artist,2))
    plt.savefig("./chart/outliers/{}.png".format(artist))
    plt.show()

def findOutliersFromClusters(artist,dx="tempo",dy="loudness",saveFigure=False):
    outlier = OutlierDetection.Outlier()
    data = dataset.getDataFromArtist(artist)
    clusters = outlier.cluster("gmm", data, n_components=2)
    if saveFigure:
        graphOutlier(clusters)
    labels = []
    for item in clusters["data"]:
        label = item["label"]
        labels.append(label)

    unique, counts = np.unique(labels, return_counts=True)
    occurrences = dict(zip(unique, counts))
    outlier_label = min(occurrences, key=lambda x: occurrences[x])
    print("label {} cluster is outlier".format(outlier_label))
    # draw graph with outlier
    data = []
    outliers = []
    outliers_data = []
    for item in clusters["data"]:
        x = item[dx]
        y = item[dy]
        label = item["label"]
        data.append([x, y])
        # plt.scatter(x=x,y=y,color=colors)

        if label == outlier_label:
            outliers.append([x, y])
            outliers_data.append(item["title"])
    data = np.array(data)
    outliers = np.array(outliers)
    return outliers,data


def findOutliersFromClustersWithSongTitle(artist,dx="tempo",dy="loudness",saveFigure=False):
    outlier = OutlierDetection.Outlier()
    data = dataset.getDataFromArtist(artist)
    clusters = outlier.cluster("gmm", data, n_components=2)
    if saveFigure:
        graphOutlier(clusters)
    labels = []
    for item in clusters["data"]:
        label = item["label"]
        labels.append(label)

    unique, counts = np.unique(labels, return_counts=True)
    occurrences = dict(zip(unique, counts))
    outlier_label = min(occurrences, key=lambda x: occurrences[x])
    # draw graph with outlier
    data = []
    outliers = []
    outliers_data = []
    for item in clusters["data"]:
        x = item[dx]
        y = item[dy]
        label = item["label"]
        data.append([x, y])
        # plt.scatter(x=x,y=y,color=colors)

        if label == outlier_label:
            outliers.append(item["title"])
    return outliers
@mpltex.acs_decorator
def outlierDetectionGMM(artist,dx="tempo",dy="loudness"):
    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[dx], data)))
    y = np.array(list(map(lambda y: y[dy], data)))

    X = np.stack((x,y),axis=-1)
    gmm = GaussianMixture(n_components=2,covariance_type="diag")
    gmm.fit(X)

    # Compute the Mahalanobis distance for each data point
    mahal_dist = gmm.score_samples(X)

    # Define a threshold for outlier detection
    outlier_thresh = np.percentile(mahal_dist, 5)
    # Identify outliers based on the Mahalanobis distance threshold
    outliers = X[mahal_dist < outlier_thresh]

    #fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    #plt.hist(mahal_dist, bins=50, edgecolor='black')

    # graph

    plt.scatter(x=x,y=y,color=mpltex.colors)
    # mark outliers
    #print(outliers.shape)
    for outlier in outliers:
        x = outlier[0]
        y = outlier[1]
        plt.scatter(x=x, y=y,marker='x',color="red",s=150)
    plt.title("{} - Outliers ({})".format(artist,len(outliers)))
    plt.show()

def gmm2(artist,dx="tempo",dy="loudness"):
    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[dx], data)))
    y = np.array(list(map(lambda y: y[dy], data)))

    # Generate some example data
    #X = np.random.randn(1000, 2)
    X = np.stack([x,y],axis=-1)
    # Fit a GMM to the data
    n_components = 2
    gmm = GaussianMixture(n_components=n_components)
    gmm.fit(X)

    # Compute the Mahalanobis distance of each point from the centroid of each component
    distances = np.zeros((X.shape[0], n_components))
    for i in range(n_components):
        mean = np.atleast_2d(gmm.means_[i])
        cov = np.squeeze(gmm.covariances_[i])
        inv_cov = np.linalg.inv(cov)
        diff = X - mean
        distances[:, i] = np.sqrt(np.sum(np.dot(diff, inv_cov) * diff, axis=1))

    # Identify the outliers as the points with the largest Mahalanobis distance across all components
    threshold = np.percentile(distances, 95)
    outliers = np.where(np.max(distances, axis=1) > threshold)[0]

    # Plot the data and outliers separately
    plt.scatter(X[:, 0], X[:, 1], c=gmm.predict(X), cmap='viridis')
    plt.scatter(X[outliers, 0], X[outliers, 1], c='red', marker='x')

    # Set the x-axis and y-axis labels
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')

    # Show the plot
    plt.show()


def drawArtists():
    mpl.rcParams['font.family'] = 'Times New Roman'
    # mpl.rcParams['font.size'] = 10

    fig, axs = plt.subplots(figsize=(3, 2))

    #First subplot
    outliers, data = findOutliersFromClusters("Blue Oyster Cult")
    axs.scatter(x=data[:, 0], y=data[:, 1], color="blue", s=10)
    axs.scatter(x=outliers[:, 0], y=outliers[:, 1], marker='x', color="red", s=50, label="Outlier")
    axs.set_title("Blue Oyster Cult")
    #
    #
    axs.legend()


    # # Second subplot
    # outliers, data = findOutliersFromClusters("Rod Lee")
    # axs.scatter(x=data[:, 0], y=data[:, 1], color="blue", s=2)
    # axs.scatter(x=outliers[:, 0], y=outliers[:, 1], marker='x', color="red", s=50, label="Outlier")
    # axs.set_title("Rod Lee")
    # axs.legend()

    axs.set_xlim(-10, 220)
    axs.set_ylim(-35,0)
    # plt.subplots_adjust(wspace=0.3)
    plt.savefig('myplot.png', dpi=500)

    plt.show()

def findFindOutliersFromArtists(artists,generateFigure=False):
    outliers_list = np.empty((0,2))
    for artist in artists:
        print("[{}]".format(artist))
        outliers,data = findOutliersFromClusters(artist,saveFigure=generateFigure)
        outliers_list = np.concatenate((outliers_list,outliers),axis=0)
    outliers_list = np.array(outliers_list)

    print("There are total {} outliers".format(outliers_list.shape[0]))
    return outliers_list

def doOutliersDetectionFromArtistList(artist_list,generateFigure=False):
    print("Task: Detecting Outliers from given artist list")
    outliers = findFindOutliersFromArtists(artist_list,generateFigure)
    print(outliers)

def read_csv_and_create_dict(input_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        output_dict = {}
        current_artist = None

        for row in reader:
            if row[0]:  # If the first column (Artist) is not empty
                current_artist = row[0]
                output_dict[current_artist] = {}
            else:
                song_title = row[1].replace(u'\xa0', u' ')
                outlier = row[2]
                #outlier_category = row[3]
                if outlier == "1":
                    output_dict[current_artist][song_title] = outlier

    return output_dict

def evaluateModel():
    # read outlier lavel csv
    #csv = pd.read_csv("./anlysis/Artist Outlier.csv")
    out = []
    labels_ground = read_csv_and_create_dict("./anlysis/Artist Outlier.csv")
    for a in labels_ground:
        artist = a
        print("Artist: {}".format(artist))

        data_all = dataset.getDataFromArtist(artist)
        data_all = list(map(lambda x: x['title'], data_all))
        outliers = [song for song, outlier in labels_ground[artist].items() if outlier == '1']

        # Create groud truth labels
        labels = {}
        for song in data_all:
            if song in outliers:
                labels[song] = 1
            else:
                labels[song] = 0
        # Create predit labels
        predicted = findOutliersFromClustersWithSongTitle(artist)
        predicted_labels = {}
        for song in data_all:
            if song in predicted:
                predicted_labels[song] = 1
            else:
                predicted_labels[song] = 0

        # Evaluate model
        TruePositive = len([song for song, label in labels.items() if label == 1 and predicted_labels[song] == 1])
        TrueNegative = len([song for song, label in labels.items() if label == 0 and predicted_labels[song] == 0])
        FalsePositive = len([song for song, label in labels.items() if label == 0 and predicted_labels[song] == 1])
        FalseNegative = len([song for song, label in labels.items() if label == 1 and predicted_labels[song] == 0])

        metrics = {}
        metrics['Artist'] = artist

        if (TruePositive + FalseNegative) != 0:
            metrics['TPR'] = round(TruePositive / (TruePositive + FalseNegative), 3)
        else:
            metrics['TPR'] = "N/A"

        if (FalsePositive + TrueNegative) != 0:
            metrics['FPR'] = round(FalsePositive / (FalsePositive + TrueNegative), 3)
        else:
            metrics['FPR'] = "N/A"

        if (TrueNegative + FalsePositive) != 0:
            metrics['TNR'] = round(TrueNegative / (TrueNegative + FalsePositive), 3)
        else:
            metrics['TNR'] = "N/A"

        if (FalseNegative + TruePositive) != 0:
            metrics['FNR'] = round(FalseNegative / (FalseNegative + TruePositive), 3)
        else:
            metrics['FNR'] = "N/A"



        print("TPR: {}, FPR: {}, TNR: {}, FNR: {}".format(metrics['TPR'], metrics['FPR'], metrics['TNR'], metrics['FNR']))
        out.append(metrics)
    csv = pd.DataFrame(out)
    print(csv)
    csv.to_csv("./anlysis/outlierdetection_result.csv",index=None)

if __name__ == '__main__':
    artist_list = [
        "The Waybacks",
    ]

    # labels_ground = read_csv_and_create_dict("./anlysis/Artist Outlier.csv")
    #
    # n_songs = 0
    # for a in labels_ground:
    #     data = dataset.getDataFromArtist(a)
    #     n_songs+= len(data)
    # print(n_songs)

    drawArtists()
    # Do cluster
    # outlier = OutlierDetection.Outlier()
    # data = dataset.getDataFromArtist("Colin Meloy")
    # clusters = outlier.cluster("gmm", data,n_components=2)

    #graphLabel(clusters)
    #graphOutlier(clusters)
    #findOutliersFromClusters("Thievery Corporation", saveFigure=True)
    #outlierDetectionGMM("The Waybacks")
    #outlierDetectionGMM("Blue Six")
    #drawArtists()
    #evaluateModel()
