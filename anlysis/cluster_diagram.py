import outlier.data as dataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def draw_artistCluster(artist, dx="tempo", dy="loudness"):
    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[dx], data)))
    y = np.array(list(map(lambda y: y[dy], data)))

    # Create an array with x and y values
    X = np.column_stack((x, y))

    # Standardize the data for better clustering performance
    X_standardized = StandardScaler().fit_transform(X)

    # Apply DBSCAN clustering algorithm
    dbscan = DBSCAN(eps=0.8)  # You can tune the eps and min_samples parameters
    clusters = dbscan.fit_predict(X_standardized)

    # Get unique cluster labels
    unique_clusters = set(clusters)

    # Define the markers for each cluster
    markers = ['o', '^', 's']  # Circle, triangle, and square

    # Plot each cluster with a different marker
    for idx, cluster in enumerate(unique_clusters):
        if cluster == -1:
            color = 'black'
            marker = 'x'
        else:
            color = plt.cm.Set1(cluster / len(unique_clusters))
            marker = markers[idx % len(markers)]

        # Get the points belonging to this cluster
        cluster_points = X[clusters == cluster]

        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=[color], marker=marker, label=f'Cluster {cluster}')

    plt.xlabel(dx)
    plt.ylabel(dy)
    plt.legend()
    plt.show()

def draw_artistClusterRaw(artist, dx="tempo", dy="loudness"):
    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[dx], data)))
    y = np.array(list(map(lambda y: y[dy], data)))
    plt.figure(dpi=300)
    plt.scatter(x=x,y=y,c="black",marker='x')
    plt.title(artist)
    plt.xlabel("Tempo")
    plt.ylabel("Loudness")
    plt.savefig("./{}_all.png".format(artist))
    plt.show()
    
if __name__ == '__main__':
    draw_artistClusterRaw("Blue Oyster Cult")