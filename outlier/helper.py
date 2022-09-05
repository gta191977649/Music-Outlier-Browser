from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def PlotElbowMethodTest(data,min_k,max_k):
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
def findOptimalKByElbowMethod(data,min_k,max_k):
    return False