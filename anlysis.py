import matplotlib.pyplot as plt
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

def graphLabel(clusters,dx="tempo",dy="loudness"):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink']
    for item in clusters["data"]:
        x = item[dx]
        y = item[dy]
        label = item["label"]
        plt.scatter(x=x,y=y,c=colors[label])
    plt.show()

def graphOutlier(clusters,dx="tempo",dy="loudness"):
    colors = ['blue',  'orange','green', 'purple', 'yellow', 'pink']
    labels = []
    for item in clusters["data"]:
        label = item["label"]
        labels.append(label)

    unique, counts = np.unique(labels, return_counts=True)
    occurrences = dict(zip(unique, counts))
    outlier_label = min(occurrences, key=lambda x: occurrences[x])
    print("label {} cluster is outlier".format(outlier_label))
    # draw graph with outlier
    for item in clusters["data"]:
        x = item[dx]
        y = item[dy]
        label = item["label"]
        plt.scatter(x=x,y=y,c=colors[label])

        if label == outlier_label:
            plt.scatter(x=x,y=y,marker='x',color="red",s=80)

    plt.show()

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

    # graph points
    plt.scatter(x=x,y=y)
    # mark outliers
    #print(outliers.shape)
    for outlier in outliers:
        x = outlier[0]
        y = outlier[1]
        plt.scatter(x=x, y=y,marker='x',color="red",s=100)
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


if __name__ == '__main__':
    artist_list = [
        "Blue Oyster Cult",
        "MNEMIC",
        "Colin Meloy",
        "Rod Lee",
        "Blue Six",
        "Chris Clark",
        "Deadmau5"
    ]
    # Do cluster
    outlier = OutlierDetection.Outlier()
    data = dataset.getDataFromArtist("MNEMIC")
    clusters = outlier.cluster("gmm", data,n_components=2)
    #graphLabel(clusters)
    graphOutlier(clusters)

    #outlierDetectionGMM("Colin Meloy")
    #outlierDetectionGMM("Blue Six")