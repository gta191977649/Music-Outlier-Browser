import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn

import outlier.data as dataset
import outlier.config as CONF
import outlier.helper as helper
import seaborn as sns
import outlier.calc as calc
import tkinter as tk
from tkinter import scrolledtext
import webbrowser
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

import scipy.stats as st

def elbowMethodTest(x,y,diagram=False):
    # K Means
    xy = np.column_stack((x, y))
    # Calculate the within-cluster sum of squares for different values of k
    wcss = []
    k_values = range(1, 10)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(xy)
        wcss.append(kmeans.inertia_)

    # Find the "elbow" in the plot
    diffs = np.diff(wcss)
    diffs2 = np.diff(diffs)
    elbow = np.argmax(diffs2) + 2

    if diagram:
        # Plot the within-cluster sum of squares as a function of k
        plt.plot(k_values, wcss, 'bx-')
        plt.plot(elbow, wcss[elbow - 1], 'ro')
        plt.xlabel('k')
        plt.ylabel('WCSS')
        plt.title('Elbow Method')
        plt.show()
        print("The optimal number of clusters is:", elbow)
    return elbow

def clusterSongsByArtist(artist,x_discriminator="tempo",y_discriminator="loudness"):

    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[x_discriminator], data)))
    y = np.array(list(map(lambda y: y[y_discriminator], data)))

    #k = elbowMethodTest(x,y)
    k = 1
    # Compute the K nearest neighbors of each point
    X = np.column_stack((x, y))
    knn = NearestNeighbors(n_neighbors=5).fit(X)
    distances, indices = knn.kneighbors(X)

    # Compute the centroid points for each cluster
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    centroids = kmeans.cluster_centers_
    distances_to_centroids = [np.linalg.norm(X[i] - centroids[kmeans.labels_[i]]) for i in range(len(X))]

    # Compute the distances from each point to the centroid of its K nearest neighbors
    distances_to_knn_centroids = [np.linalg.norm(X[i] - np.mean(X[indices[i]], axis=0)) for i in range(len(X))]

    # Identify the outliers as points with distance greater than some threshold
    outlier_threshold = np.percentile(distances_to_knn_centroids, 96)
    outliers = X[distances_to_knn_centroids > outlier_threshold]

    # Plot the results
    seaborn.kdeplot(x=X[:, 0], y=X[:, 1],levels=1)
    plt.scatter(X[:, 0], X[:, 1], color='b')
    plt.scatter(outliers[:, 0], outliers[:, 1], color='r', marker='x', s=100)
    for centroid in centroids:
        plt.scatter(centroid[0],centroid[1],c="red")
    plt.title('Outlier')
    plt.show()

def kde(artist,x_discriminator="tempo",y_discriminator="loudness"):
    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[x_discriminator], data)))
    y = np.array(list(map(lambda y: y[y_discriminator], data)))
    size = 10
    xmin, xmax = -size, size
    ymin, ymax = -size, size

    # Peform the kernel density estimate
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Contourf plot
    cfset = ax.contourf(xx, yy, f, cmap='Blues')
    ## Or kernel density estimate plot instead of the contourf plot
    # ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
    # Contour plot
    cset = ax.contour(xx, yy, f, colors='k')
    # Label plot
    ax.clabel(cset, inline=1, fontsize=10)
    ax.set_xlabel('Y1')
    ax.set_ylabel('Y0')

    plt.show()