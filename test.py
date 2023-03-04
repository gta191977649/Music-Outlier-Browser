import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
def plot_subplots(N):
    # Generate some sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Calculate the number of rows and columns
    nrows = N // 2
    ncols = N // 2 + N % 2

    # Create a grid of subplots
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)

    # Flatten the axs array to simplify the loop
    axs = axs.ravel()

    # Loop over the subplots and plot the data
    for i in range(N):
        axs[i].plot(x, y)
        axs[i].set_title(f'Plot {i+1}')

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Display the plots
    plt.show()
plot_subplots(5)