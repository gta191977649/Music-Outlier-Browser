import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generate some sample data
data = np.random.rand(100, 2)

# Create a two-dimensional KDE
kde = KernelDensity(bandwidth=0.2, kernel='gaussian')
kde.fit(data)

# Generate cluster assignments using k-means
kmeans = KMeans(n_clusters=3)
cluster_assignments = kmeans.fit_predict(data)

# Create an empty array for each cluster
cluster_arrays = [[] for _ in range(3)]

# Assign each point to the appropriate cluster
for i, point in enumerate(data):
    # Compute the probability density function for this point
    log_prob = kde.score_samples(point.reshape(1, -1))
    # Assign the point to the cluster with the highest probability density
    cluster = np.argmax(log_prob)
    cluster_arrays[cluster].append(point)

# Visualize the clusters
fig, ax = plt.subplots(figsize=(8, 6))


ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Clustered Data')
plt.show()
