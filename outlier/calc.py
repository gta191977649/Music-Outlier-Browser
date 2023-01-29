import numpy as np
import math

def gauss_kernel(x):
    return 1/math.sqrt(2*math.pi) * math.exp(-0.5 * math.pow(x,2))

def get_kde(x,data,kernel,bandwidth):
    N = len(data)
    res = 0
    for i in range (0,N):
        res += kernel((x - data[i]) / bandwidth)
    res /= (N * bandwidth)
    return res

# KDE calculation
def kde(data,kernel=gauss_kernel,bandwidth=0.1,n=50):
    x = np.linspace(min(data),max(data),num=n)
    y = []
    for i in range (0,len(x)):
        val = get_kde(x[i], data, kernel, bandwidth)
        y.append(val)
    return x,y


# x,y = kde([1,2,3],kernel=gauss_kernel,bandwidth=0.1)
