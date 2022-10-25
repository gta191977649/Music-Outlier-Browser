from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plotElbowMethodTest(data,min_k,max_k):
    n_of_clusters = range(min_k, max_k)
    inertias = []
    for i in n_of_clusters:
        knn = KMeans(n_clusters=i)
        knn.fit(data)
        inertias.append(knn.inertia_)
    plt.plot(n_of_clusters, inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

def plotScatterGraph(data,x_discriminator="tempo",y_discriminator="loudness"):
    x = np.array(list(map(lambda x: x[x_discriminator], data)))
    y = np.array(list(map(lambda y: y[y_discriminator], data)))
    plt.scatter(x, y)
    plt.show()

def plotScatterClusterGraph(labels,x):
    # debug plot
    colors = sns.color_palette("Set2", len(x))

    print(len(labels))
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    for i in range(len(x)):
        plt.scatter(x=x[i][0],y=x[i][1],c=colors[labels[i]])
    plt.title("Estimated number of clusters: %d" % n_clusters_)
    plt.show()
def findOptimalKByElbowMethod(data,min_k,max_k):
    return False

# This function removes the special charactor occcur in path
def escapePath(path):
    chars = [
        "\"",
        "\\",
        "/",
        " "
    ]
    path = path.strip()
    for char in chars: path = path.replace(char,"")
    return path
