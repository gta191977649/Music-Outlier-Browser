from tslearn.metrics import dtw_path
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import seaborn as sns
import matplotlib
#matplotlib.rcParams['font.family'] = 'TakaoPGothic'
import librosa
def plotDTW(signal_1, signal_2):
    # Reshape the signals
    signal_1 = signal_1.reshape(-1, 1)
    signal_2 = signal_2.reshape(-1, 1)

    # Calculate the DTW path
    path, sim = dtw_path(signal_1, signal_2)

    # Extract the path coordinates
    path_1 = [i[0] for i in path]
    path_2 = [i[1] for i in path]

    # Calculate the similarity matrix
    similarity_matrix = cdist(signal_1, signal_2)

    # Create the figure and subplots
    plt.figure(1, figsize=(8, 8))
    left, bottom = 0.01, 0.1
    w_ts = h_ts = 0.2
    left_h = left + w_ts + 0.02
    width = height = 0.65
    bottom_h = bottom + height + 0.02

    rect_s_y = [left, bottom, w_ts, height]
    rect_gram = [left_h, bottom, width, height]
    rect_s_x = [left_h, bottom_h, width, h_ts]

    ax_gram = plt.axes(rect_gram)
    ax_s_x = plt.axes(rect_s_x)
    ax_s_y = plt.axes(rect_s_y)

    # Plot the similarity matrix and the DTW path
    ax_gram.imshow(similarity_matrix, cmap='gray_r', origin='lower')
    ax_gram.set_xlabel('Reference Signal')
    ax_gram.set_ylabel('Dependent Signal')
    ax_gram.plot(path_2, path_1, 'r-', linewidth=3.)

    # Plot the reference signal
    ax_s_x.plot(signal_1, label='Reference Signal', color='black', linewidth=2.)
    ax_s_x.set_xlim([0, len(signal_1) - 1])
    ax_s_x.set_xlabel('Time')
    ax_s_x.set_ylabel('Amplitude')

    # Plot the dependent signal
    ax_s_y.plot(-signal_2, np.arange(len(signal_2)), label='Dependent Signal', color='black', linewidth=2.)
    ax_s_y.set_ylim([0, len(signal_2) - 1])
    ax_s_y.set_xlabel('Amplitude')
    ax_s_y.set_ylabel('Time')

    plt.tight_layout()
    plt.show()

    return sim


def plot_aggregated_score_with_outliers(contrast_matrix):
    # Create an array of section indices
    sections = np.arange(len(contrast_matrix))

    # Calculate Q1, Q3, and IQR for outlier detection
    Q1 = np.percentile(contrast_matrix, 25)
    Q3 = np.percentile(contrast_matrix, 75)
    IQR = Q3 - Q1

    # Define the bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = np.where((contrast_matrix < lower_bound) | (contrast_matrix > upper_bound))

    # Plot the contrast scores for each section
    plt.bar(sections, contrast_matrix, label='Contrast Scores', alpha=0.7, width=0.6)

    # Highlight the outliers in red with higher alpha and slightly smaller width for emphasis
    plt.bar(sections[outliers], np.array(contrast_matrix)[outliers], color='red', label='Outliers', alpha=1.0,
            width=0.5)

    # Set the title and labels
    plt.title("Section Contrast Scores with Highlighted Outliers")
    plt.xlabel("Song Index")
    plt.ylabel("Contrast Score")
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_kde_with_outliers(contrast_matrix):
    # Calculate Q1, Q3, and IQR for outlier detection
    Q1 = np.percentile(contrast_matrix, 25)
    Q3 = np.percentile(contrast_matrix, 75)
    IQR = Q3 - Q1

    # Define the bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = np.where((contrast_matrix < lower_bound) | (contrast_matrix > upper_bound))

    print("Outliers")
    print(outliers)
    # Plot KDE for the contrast scores
    sns.kdeplot(contrast_matrix, fill=True, label='Contrast Scores', alpha=0.7)

    # Plot the outliers as individual data points in red
    sns.rugplot(np.array(contrast_matrix)[outliers], color='red', height=0.1, label='Outliers')

    # Set the title and labels
    plt.title("Kernel Density Estimation of Contrast Scores with Highlighted Outliers")
    plt.xlabel("Contrast Score")
    plt.ylabel("Density")
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_histogram_and_bars(songs, outliers):
    scores = [song["score"] for song in songs]
    outlier_scores = [outlier["score"] for outlier in outliers]

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Histogram of scores
    ax[0].hist(scores, bins=30, alpha=0.7, color='b', edgecolor='black', label='Normal Values')
    ax[0].hist(outlier_scores, bins=30, alpha=0.7, color='r', edgecolor='black', label='Outliers')
    ax[0].set_title('Histogram of Contrast Scores')
    ax[0].set_xlabel('Contrast Score')
    ax[0].set_ylabel('Frequency')
    ax[0].legend()

    # Bar plot with scores against indices
    sections = np.arange(len(scores))
    colors = ['r' if song in outliers else 'b' for song in songs]
    ax[1].bar(sections, scores, alpha=0.7, color=colors)
    ax[1].set_title('Bar Plot of Contrast Scores against Indices')
    ax[1].set_xlabel('Song Index')
    ax[1].set_ylabel('Contrast Score')

    plt.tight_layout()
    plt.show()

def plot_signals(signals, labels=None,title=None):
    """
    Plot multiple signals on the same plot.

    Parameters:
    signals (list of np.array): List of signals to plot.
    labels (list of str, optional): List of labels for each signal. Defaults to None.
    """
    # Create a color cycle iterator using the default property cycle
    color_cycle = plt.cm.viridis(np.linspace(0, 1, len(signals)))

    plt.figure(figsize=(10, 6))
    for idx, signal in enumerate(signals):
        color = color_cycle[idx]
        label = labels[idx] if labels else f'Signal {idx+1}'
        #plt.plot(signal, label=label, color=color)
        plt.plot(signal, label=label)

    plt.xlabel('Time (frames)')
    plt.ylabel('Amplitude (dB)')
    plt.legend(loc='upper right')
    plt.title('Filter Bank Test\n{}'.format(title))
    plt.grid(True)
    plt.show()

def seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{minutes:02d}:{seconds:02.0f}"
def plot_signals_by_sections(sections,title=None):
    # Create two subplots with different heights using gridspec_kw
    fig, axs = plt.subplots(2, 1, figsize=(7, 5), sharex=True, gridspec_kw={'height_ratios': [3, 0.2]})

    colors = plt.cm.tab20(np.linspace(0, 1, len(sections)))  # Generates a color map

    for idx, section in enumerate(sections):
        start_time, end_time = section['time']
        feature = section['feature']

        # Create an array representing the time in seconds for this section
        time_array = np.linspace(start_time, end_time, len(feature))

        # Plotting each section with a different color in the first subplot
        axs[0].plot(time_array, feature, label=f'Section {section["label"]}', color=colors[idx])

        # Drawing vertical bars to indicate sections in the second subplot
        axs[1].axvspan(start_time, end_time, color=colors[idx], alpha=0.5)
        # Adding section label text in the center of each rectangle
        center_time = (start_time + end_time) / 2
        axs[1].text(center_time, 0.5, section["label"], ha='center', va='center')

        # Adding vertical grey dashed lines to indicate section boundaries in the top signal plot
        axs[0].axvline(x=start_time, color='grey', linestyle='--', linewidth=1,alpha=0.5)
        axs[0].axvline(x=end_time, color='grey', linestyle='--', linewidth=1,alpha=0.5)

    axs[0].set_ylabel('Feature Value')
    axs[0].set_title('{}\nSection Structure Analysis'.format(title))
    # axs[0].legend(loc='lower left')
    axs[0].grid(False)

    axs[1].set_xlabel('Time (mm:ss)')
    axs[1].set_yticks([])  # Hide y-axis ticks and labels for the second subplot
    axs[1].set_xlim([0, np.max([section['time'][1] for section in sections])])  # Set x-axis limits

    # Format x-axis labels as mm:ss
    axs[1].set_xticks(
        np.arange(0, np.max([section['time'][1] for section in sections]) + 1, step=60))  # Set x-ticks every 60 seconds
    axs[1].set_xticklabels([seconds_to_mmss(t) for t in axs[1].get_xticks()])

    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()
