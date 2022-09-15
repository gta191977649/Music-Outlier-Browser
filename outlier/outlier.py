from ast import Delete
from cgi import test
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import data as dataset
import helper as helper
import numpy as np
import config as CONF
import seaborn as sns
from sklearn.cluster import MeanShift

class Outlier:

    def detect(self,method="mean_shift",data=[]):
        algorithms = {
            "mean_shift": self.mean_shift,
        }
        if not method in algorithms: raise(Exception("Unknown detection algorithms!"))
        data = np.array(data)
        return algorithms[method](data)

    def mean_shift(self,data):
        clustering = MeanShift(bandwidth=2).fit(data)
        return clustering.labels_
    def artist(self,artist,x_discriminator,y_discriminator = None):
        # Obtain data from dataset
        results = dataset.getDataFromArtist(artist)
        
        # Processing Data and normalisation
        x = np.array(list(map(lambda x: x[x_discriminator] , results)))
        x_1 = (x-np.mean(x))/np.std(x)
        y = np.array(list(map(lambda y: y[y_discriminator] , results)))
        y_1 = (y-np.mean(y))/np.std(y)
        data = np.array(list(zip(x_1, y_1)))
        
        # calculate the distance for every point to origin
        dist = []
        for i in range (0,len(data)):
            dist.append(np.sqrt((data[i,0])**2+(data[i,1])**2))
        
        dist_mean = np.mean(dist)
        dist_std = np.std(dist)

        
        # 99.7% confidence level --> 3*sigma; 95% confidence level --> 2*sigma;
        anomaly_cut_off = dist_std * 3 # 95% ~ 99.7%
        lower_limit = dist_mean - anomaly_cut_off
        upper_limit = dist_mean + anomaly_cut_off
        
        # Generate outliers
        anomalies = []
        idx = 0
        neg_data = []
        for outlier in dist:
            if outlier > upper_limit or outlier < lower_limit:
                anomalies.append(outlier)
                neg_data.append(data[idx])
                np.delete(data,idx)
            idx += 1
            
        neg_data = np.array(neg_data)
        pos_data = data
        
        # Plot Result
        colors = ["#B2A4FF","#FF0000"]
        # Positive data
        plt.scatter(pos_data[:,0],pos_data[:,1],color=colors[0])
        # Negative data
        plt.scatter(neg_data[:,0],neg_data[:,1],color=colors[1])
        plt.show()
       

        # Plot Result
        # colors = ["#B2A4FF","#FFB4B4"]
        # for idx,point in enumerate(data):
        #     x,y = point
        #     label = labels[idx]
        #     plt.scatter(x=x, y=y)
        # plt.show()
        return anomalies

    def artist_method_2(self,artist,x_discriminator,y_discriminator = None):
        # Obtain data from dataset
        results = dataset.getDataFromArtist(artist)

        # Processing Data and normalisation
        x = np.array(list(map(lambda x: x[x_discriminator] , results)))
        x_1 =(x-np.mean(x))/np.std(x)
        y = np.array(list(map(lambda y: y[y_discriminator] , results)))
        y_1 =(y-np.mean(y))/np.std(y)
        data = np.array(list(zip(x_1, y_1)))
        
        # calculate distance and sort to reconstruct the data
        list_dist = []
        for i in range(data.shape[0]):
            list_dist.append(np.sqrt(data[i, 0]**2 + data[i, 1]**2))
        
        list_xy = list(zip(x_1, y_1))
        list_sorted = sorted(list(zip(list_dist,list_xy)), key=lambda x: x[0], reverse=True)
        list_xy = list(map(lambda x: x[1], list_sorted))
        
        x_1 = np.array(list(map(lambda x: x[0], list_xy)))
        y_1 = np.array(list(map(lambda x: x[1], list_xy)))
        data = np.array(list(zip(x_1, y_1)))
        
        # calculate the distance for every point to origin but exclude one point every time
        dist = []
        print(data[0,:])
        for i in range (0,len(data)-1):
            temp = []
            temp = data[i:, :]
            dist_temp = []
            for j in range (0,len(temp)):
                dist_temp.append(np.sqrt((temp[j,0])**2+(temp[j,1])**2))
            dist.append(np.mean(dist_temp))
            
        # calculate the distance between two elements
        dist_delta = []
        for i in range (0,len(dist)-1):
            dist_delta.append(dist[i+1] - dist[i])
            
        dist_delta_mean = np.mean(dist_delta)
        dist_delta_std = np.std(dist_delta)
        print(dist_delta_mean)
        print(dist_delta_std)
        
        anomaly_cut_off = dist_delta_std * 2.5
        lower_limit = dist_delta_mean - anomaly_cut_off
        upper_limit = dist_delta_mean + anomaly_cut_off
        
        # Generate outliers
        anomalies = []
        idx = 0
        neg_data = []
        for outlier in dist_delta:
            if outlier > upper_limit or outlier < lower_limit:
                anomalies.append(outlier)
                neg_data.append(data[idx])
                np.delete(data,idx)
            idx += 1
            
        neg_data = np.array(neg_data)
        pos_data = data

        # idx = [i for i in range(len(dist)-1)]
        # plt.scatter(idx, dist_delta)
        # plt.show()
        # Plot Result
        colors = ["#B2A4FF","#FFB4B4"]
        # Positive data
        plt.scatter(pos_data[:,0],pos_data[:,1],color=colors[0])
        # Negative data
        plt.scatter(neg_data[:,0],neg_data[:,1],color=colors[1])
        plt.show()

