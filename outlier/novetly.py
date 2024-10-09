from scipy.spatial.distance import pdist, squareform
import numpy as np
import librosa
import matplotlib.pyplot as plt
import libfmp.c3
import scipy
import signal

def calculate_ki_chroma(chromagram):
    """Calculate a key-invariant chromagram for a given audio waveform."""
    chroma_vals = np.sum(chromagram, axis=1)
    maj_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    min_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    maj_corrs = np.correlate(chroma_vals, maj_profile, mode='same')
    min_corrs = np.correlate(chroma_vals, min_profile, mode='same')
    key_shift = np.argmax(np.concatenate((maj_corrs, min_corrs))) % 12
    return np.roll(chromagram, -key_shift, axis=0)


def plot_chroma(chroma, sr, hop_length, title='Key-Invariant Chromagram'):
    """Plot the key-invariant chromagram."""
    plt.figure(figsize=(18, 5))
    librosa.display.specshow(chroma,sr=sr, hop_length=hop_length, x_axis='time', y_axis='chroma')
    plt.title(title)
    plt.tight_layout()
    plt.show()

def plot_ssm(ssm, title='Self-Similarity Matrix'):
    """Plot the self-similarity matrix."""
    plt.figure(figsize=(8, 8))
    plt.imshow(ssm, cmap='hot', interpolation='nearest')
    plt.title(title)
    plt.xlabel('Frame Index')
    plt.ylabel('Frame Index')
    plt.tight_layout()
    plt.show()

def plot_novelty_with_peaks(nov, peaks_lag, title='Smoothed Novelty Curve with Peaks'):
    """Plot the novelty curve with peaks highlighted."""
    plt.figure(figsize=(12, 3))
    plt.plot(nov, label='Novelty Curve', color='blue')
    plt.plot(peaks_lag, nov[peaks_lag], "ro", label='Peaks')  # Highlight peaks with red points
    plt.title(title)
    plt.xlabel('Frame Index')
    plt.ylabel('Novelty Value')
    plt.axhline(y=0, color='r', linestyle='--')  # Add a reference line at y=0
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
def plot_curve(data, title='Smoothed Novelty Curve'):
    plt.figure(figsize=(10, 2))
    plt.plot(data, label=title, color='blue')
    plt.title('Smoothed Novelty Curve (Lag)')
    plt.xlabel('Frame Index')
    plt.ylabel('Novelty Value')
    plt.axhline(y=0, color='r', linestyle='--')  # Add a reference line at y=0
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def smooth_downsample_feature_sequence(X, Fs, filt_len=41, down_sampling=10, w_type='boxcar'):
    """Smoothes and downsamples a feature sequence. Smoothing is achieved by convolution with a filter kernel

    Notebook: C3/C3S1_FeatureSmoothing.ipynb

    Args:
        X (np.ndarray): Feature sequence
        Fs (scalar): Frame rate of ``X``
        filt_len (int): Length of smoothing filter (Default value = 41)
        down_sampling (int): Downsampling factor (Default value = 10)
        w_type (str): Window type of smoothing filter (Default value = 'boxcar')

    Returns:
        X_smooth (np.ndarray): Smoothed and downsampled feature sequence
        Fs_feature (scalar): Frame rate of ``X_smooth``
    """
    filt_kernel = np.expand_dims(signal.get_window(w_type, filt_len), axis=0)
    X_smooth = signal.convolve(X, filt_kernel, mode='same') / filt_len
    X_smooth = X_smooth[:, ::down_sampling]
    Fs_feature = Fs / down_sampling
    return X_smooth, Fs_feature
def plot_ssm_with_segments(ssm, peaks_lag, title='Self-Similarity Matrix with Segments'):
    """Plot the self-similarity matrix with segment boundaries overlayed."""
    plt.figure(figsize=(8, 8))
    plt.imshow(ssm, cmap='hot', interpolation='nearest')

    # Overlay segment boundaries on the SSM
    for peak in peaks_lag:
        plt.axvline(x=peak, color='black', linestyle='--', lw=3)  # Vertical line for segment boundary
        plt.axhline(y=peak, color='black', linestyle='--', lw=3)  # Horizontal line for segment boundary

    plt.title(title)
    plt.xlabel('Frame Index')
    plt.ylabel('Frame Index')
    plt.tight_layout()
    plt.show()

def compute_SSM(X, Y):
    S = np.dot(np.transpose(X), Y)
    return S
def compute_kernel_checkerboard_gaussian(L, var=1, normalize=True):
    taper = np.sqrt(1/2) / (L * var)
    axis = np.arange(-L, L+1)
    gaussian1D = np.exp(-taper**2 * (axis**2))
    gaussian2D = np.outer(gaussian1D, gaussian1D)
    kernel_box = np.outer(np.sign(axis), np.sign(axis))
    kernel = kernel_box * gaussian2D
    if normalize:
        kernel = kernel / np.sum(np.abs(kernel))
    return kernel
def compute_novelty_ssm(S, kernel=None, L=10, var=0.5, exclude=False):
    """Compute novelty function from SSM [FMP, Section 4.4.1]

    Notebook: C4/C4S4_NoveltySegmentation.ipynb

    Args:
        S (np.ndarray): SSM
        kernel (np.ndarray): Checkerboard kernel (if kernel==None, it will be computed) (Default value = None)
        L (int): Parameter specifying the kernel size M=2*L+1 (Default value = 10)
        var (float): Variance parameter determing the tapering (epsilon) (Default value = 0.5)
        exclude (bool): Sets the first L and last L values of novelty function to zero (Default value = False)

    Returns:
        nov (np.ndarray): Novelty function
    """
    if kernel is None:
        kernel = compute_kernel_checkerboard_gaussian(L=L, var=var)
    N = S.shape[0]
    M = 2*L + 1
    nov = np.zeros(N)
    # np.pad does not work with numba/jit
    S_padded = np.pad(S, L, mode='constant')

    for n in range(N):
        # Does not work with numba/jit
        nov[n] = np.sum(S_padded[n:n+M, n:n+M] * kernel)
    if exclude:
        right = np.min([L, N])
        left = np.max([0, N-L])
        nov[0:right] = 0
        nov[left:N] = 0

    return nov


def frames_to_time(frame_indices, Fs_feature):
    """
    Convert an array of downsampled frame indices to time in seconds using Fs_feature.

    Args:
        frame_indices (array-like): An array of downsampled frame indices to convert.
        Fs_feature (float): The frame rate of the downsampled feature sequence.

    Returns:
        np.ndarray: An array of corresponding times in seconds.
    """
    # Convert the frame indices to a NumPy array for vectorized operations
    frame_indices = np.array(frame_indices)

    # Calculate the time in seconds for each frame index
    times_in_seconds = frame_indices / Fs_feature

    return times_in_seconds

def detect_novelty(path):
    audio_path = path

    hop_length = 128
    sr = 22050
    y, sr = librosa.load(audio_path, sr=sr)
    # y, y_perc = librosa.effects.hpss(y)
    # duration = librosa.get_duration(y=y, sr=sr, hop_length=hop_length)

    X = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length, tuning=0, norm=2)
    X = calculate_ki_chroma(X)

    X, frame_rate = libfmp.c3.smooth_downsample_feature_sequence(X, sr / hop_length, filt_len=41, down_sampling=10)
    # chroma = libfmp.c3.normalize_feature_sequence(chroma, norm='2', threshold=0.001)

    ssm = compute_SSM(X, X)

    # Compute Novetly
    nov = compute_novelty_ssm(ssm, L=20, exclude=True)

    peaks_lag, _ = scipy.signal.find_peaks(nov, prominence=0.04)


    peaks_lag_time = frames_to_time(peaks_lag, frame_rate)
    return peaks_lag_time,ssm,nov,peaks_lag,frame_rate