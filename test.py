import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

# Generate some example data
X = np.random.randn(1000, 2)

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
