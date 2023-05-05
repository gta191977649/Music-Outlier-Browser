import seaborn as sns
import matplotlib.pyplot as plt
import outlier.data as dataset
import numpy as np

def kde_artist(artist, dx="tempo", dy="loudness", dpi=300, figsize=(8, 6), pad=0.2, boundary=0.5):
    high = 127

    data = dataset.getDataFromArtist(artist)
    x = np.array(list(map(lambda x: x[dx], data)))
    y = np.array(list(map(lambda y: y[dy], data)))

    # Set font family
    plt.rcParams['font.family'] = 'Times New Roman'

    # Create a new figure with two subplots, one for the KDE plot and one for the scatter plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=dpi, gridspec_kw={'width_ratios': [3, 2]})

    # Generate the kernel density estimation and plot it on the first subplot
    sns.kdeplot(x=x, color='black', ax=ax1)

    # Find the peak points of the density curve
    peak_points = ax1.get_lines()[0].get_data()

    max_values = []
    # Add red squares for each peak point and display their values
    for i in range(len(peak_points[0])):
        if i > 0 and i < len(peak_points[0])-1 and peak_points[1][i] > peak_points[1][i-1] and peak_points[1][i] > peak_points[1][i+1]:
            ax1.plot(peak_points[0][i], peak_points[1][i], 'o', color="red")
            ax1.text(peak_points[0][i], peak_points[1][i], f"{peak_points[0][i]:.2f}", ha='left', va='bottom', fontsize=14)
            max_values.append(peak_points[0][i])

    # Add a title and labels to the first subplot
    ax1.set_xlabel(dx.capitalize(), fontsize=12)
    ax1.set_ylabel("Density", fontsize=12)

    # Filter the scatter data to only include points within the specified range of each peak value
    x_filtered = np.concatenate([x[(x >= high - boundary) & (x <= high + boundary)] for peak in peak_points[0]])
    y_filtered = np.concatenate([y[(x >= high - boundary) & (x <= high + boundary)] for peak in peak_points[0]])

    # Create a scatter plot on the second subplot showing the distribution of all x and y values
    ax2.scatter(x, y, color='black', marker='.')

    # Highlight the filtered points within the specified range of each peak value in red
    #ax2.scatter(x_filtered, y_filtered, color='red', marker='.')

    # Add labels to the second subplot
    ax2.set_xlabel(dx.capitalize(), fontsize=12)
    ax2.set_ylabel(dy.capitalize(), fontsize=12)

    fig.suptitle(f"{artist} (Discriminator: {dx})", fontweight='bold', ha='center', fontsize=18)

    plt.savefig(f"{artist}.png", dpi=dpi, bbox_inches='tight', pad_inches=pad)
    # Show the plot
    plt.show()


if __name__ == '__main__':
    kde_artist(artist="Colin Meloy",dx="loudness",dy="tempo",boundary=10)
