from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import data as dataset
import helper as helper

class Outlier:
    def artist(self,artist,x_discriminator,y_discriminator = None):
        # Obtain data from dataset
        results = dataset.getDataFromArtist(artist)

        # Processing Data
        x = list(map(lambda x: x[x_discriminator] , results))
        y = list(map(lambda y: y[y_discriminator] , results))
        data = list(zip(x, y))
        
        # Do Knn
        knn = KMeans(n_clusters=2,tol=0.000000001)
        knn.fit(data)
        centroids = knn.cluster_centers_
        labels = knn.labels_

        # Plot Result
        colors = ["#B2A4FF","#FFB4B4"]
        for idx,point in enumerate(data):
            x,y = point
            label = labels[idx]
            plt.scatter(x=x, y=y,c=colors[label])
        plt.show()