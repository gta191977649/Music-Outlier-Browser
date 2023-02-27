import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load the data
tips = sns.load_dataset("tips")

# Plot the 2D kernel density estimate of the data
sns.kdeplot(x="total_bill", y="tip", data=tips,levels=1)

# Cluster the data points using KMeans
X = tips[["total_bill", "tip"]]
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# Get the labels for each data point
labels = kmeans.labels_

# Plot the clusters and visualize the data points in each cluster
sns.scatterplot(x="total_bill", y="tip", hue=labels, data=tips, palette="colorblind")
plt.show()

# Get the data points in each cluster
cluster_0 = X[labels == 0]
cluster_1 = X[labels == 1]
cluster_2 = X[labels == 2]

print("Cluster 0:")
print(cluster_0)
print("Cluster 1:")
print(cluster_1)
print("Cluster 2:")
print(cluster_2)
