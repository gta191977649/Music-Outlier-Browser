import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture

# Generate some example data
X, y = make_blobs(n_samples=1000, centers=3, random_state=42)


# Generate some example data
X = X

# Fit a Gaussian Mixture Model with two components
gmm = GaussianMixture(n_components=3)
gmm.fit(X)

# Get the cluster labels for each data point
labels = gmm.predict(X)

# Create a list of arrays, where each array contains the data points for a given cluster
clusters = []
for i in range(gmm.n_components):
    cluster_i = X[labels == i]
    clusters.append(cluster_i)

# Print the number of data points in each cluster
for i in range(gmm.n_components):
    print("Cluster", i, "contains", len(clusters[i]), "data points.")

# Plot each cluster in a different color
for i in range(gmm.n_components):
    plt.scatter(clusters[i][:, 0], clusters[i][:, 1])

plt.show()