import librosa
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import signal
from scipy.ndimage import filters
import libfmp.b # We probally want to remove this lib on deployment stage
import libfmp.c4
import datetime

import math
# -------- [ FEATURE ] ----------
def normalize_feature_sequence(X, norm='2', threshold=0.0001, v=None):
    """Normalizes the columns of a feature sequence

    Notebook: C3/C3S1_FeatureNormalization.ipynb

    Args:
        X (np.ndarray): Feature sequence
        norm (str): The norm to be applied. '1', '2', 'max' or 'z' (Default value = '2')
        threshold (float): An threshold below which the vector ``v`` used instead of normalization
            (Default value = 0.0001)
        v (float): Used instead of normalization below ``threshold``. If None, uses unit vector for given norm
            (Default value = None)

    Returns:
        X_norm (np.ndarray): Normalized feature sequence
    """
    assert norm in ['1', '2', 'max', 'z']

    K, N = X.shape
    X_norm = np.zeros((K, N))

    if norm == '1':
        if v is None:
            v = np.ones(K, dtype=np.float64) / K
        for n in range(N):
            s = np.sum(np.abs(X[:, n]))
            if s > threshold:
                X_norm[:, n] = X[:, n] / s
            else:
                X_norm[:, n] = v

    if norm == '2':
        if v is None:
            v = np.ones(K, dtype=np.float64) / np.sqrt(K)
        for n in range(N):
            s = np.sqrt(np.sum(X[:, n] ** 2))
            if s > threshold:
                X_norm[:, n] = X[:, n] / s
            else:
                X_norm[:, n] = v

    if norm == 'max':
        if v is None:
            v = np.ones(K, dtype=np.float64)
        for n in range(N):
            s = np.max(np.abs(X[:, n]))
            if s > threshold:
                X_norm[:, n] = X[:, n] / s
            else:
                X_norm[:, n] = v

    if norm == 'z':
        if v is None:
            v = np.zeros(K, dtype=np.float64)
        for n in range(N):
            mu = np.sum(X[:, n]) / K
            sigma = np.sqrt(np.sum((X[:, n] - mu) ** 2) / (K - 1))
            if sigma > threshold:
                X_norm[:, n] = (X[:, n] - mu) / sigma
            else:
                X_norm[:, n] = v

    return X_norm
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

# -------- [ NOVELTY ] ----------
def compute_kernel_checkerboard_gaussian(L, var=1, normalize=True):
    """Compute Guassian-like checkerboard kernel [FMP, Section 4.4.1].
    See also: https://scipython.com/blog/visualizing-the-bivariate-gaussian-distribution/

    Notebook: C4/C4S4_NoveltySegmentation.ipynb

    Args:
        L (int): Parameter specifying the kernel size M=2*L+1
        var (float): Variance parameter determing the tapering (epsilon) (Default value = 1.0)
        normalize (bool): Normalize kernel (Default value = True)

    Returns:
        kernel (np.ndarray): Kernel matrix of size M x M
    """
    taper = np.sqrt(1/2) / (L * var)
    axis = np.arange(-L, L+1)
    gaussian1D = np.exp(-taper**2 * (axis**2))
    gaussian2D = np.outer(gaussian1D, gaussian1D)
    kernel_box = np.outer(np.sign(axis), np.sign(axis))
    kernel = kernel_box * gaussian2D
    if normalize:
        kernel = kernel / np.sum(np.abs(kernel))
    return kernel
# -------- [ PEAKS ] ----------
def peak_picking_simple(x, threshold=None):
    """Peak picking strategy looking for positions with increase followed by descrease

    Notebook: C6/C6S1_PeakPicking.ipynb

    Args:
        x (np.ndarray): Input function
        threshold (float): Lower threshold for peak to survive

    Returns:
        peaks (np.ndarray): Array containing peak positions
    """
    peaks = []
    if threshold is None:
        threshold = np.min(x) - 1
    for i in range(1, x.shape[0] - 1):
        if x[i - 1] < x[i] and x[i] > x[i + 1]:
            if x[i] >= threshold:
                peaks.append(i)
    peaks = np.array(peaks)
    return peaks

def peak_picking_MSAF(x, median_len=16, offset_rel=0.05, sigma=4.0):
    """Peak picking strategy following MSFA using an adaptive threshold (https://github.com/urinieto/msaf)

    Notebook: C6/C6S1_PeakPicking.ipynb

    Args:
        x (np.ndarray): Input function
        median_len (int): Length of media filter used for adaptive thresholding (Default value = 16)
        offset_rel (float): Additional offset used for adaptive thresholding (Default value = 0.05)
        sigma (float): Variance for Gaussian kernel used for smoothing the novelty function (Default value = 4.0)

    Returns:
        peaks (np.ndarray): Peak positions
        x (np.ndarray): Local threshold
        threshold_local (np.ndarray): Filtered novelty curve
    """
    offset = x.mean() * offset_rel
    x = filters.gaussian_filter1d(x, sigma=sigma)
    threshold_local = filters.median_filter(x, size=median_len) + offset
    peaks = []
    for i in range(1, x.shape[0] - 1):
        if x[i - 1] < x[i] and x[i] > x[i + 1]:
            if x[i] > threshold_local[i]:
                peaks.append(i)
    peaks = np.array(peaks)
    return peaks, x, threshold_local
# -------- [ SSM ] ----------
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
def filter_diag_sm(S, L):
    """Path smoothing of similarity matrix by forward filtering along main diagonal

    Notebook: C4/C4S2_SSM-PathEnhancement.ipynb

    Args:
        S (np.ndarray): Similarity matrix (SM)
        L (int): Length of filter

    Returns:
        S_L (np.ndarray): Smoothed SM
    """
    N = S.shape[0]
    M = S.shape[1]
    S_L = np.zeros((N, M))
    S_extend_L = np.zeros((N + L, M + L))
    S_extend_L[0:N, 0:M] = S
    for pos in range(0, L):
        S_L = S_L + S_extend_L[pos:(N + pos), pos:(M + pos)]
    S_L = S_L / L
    return S_L
def filter_diag_mult_sm(S, L=1, tempo_rel_set=np.asarray([1]), direction=0):
    """Path smoothing of similarity matrix by filtering in forward or backward direction
    along various directions around main diagonal.
    Note: Directions are simulated by resampling one axis using relative tempo values

    Notebook: C4/C4S2_SSM-PathEnhancement.ipynb

    Args:
        S (np.ndarray): Self-similarity matrix (SSM)
        L (int): Length of filter (Default value = 1)
        tempo_rel_set (np.ndarray): Set of relative tempo values (Default value = np.asarray([1]))
        direction (int): Direction of smoothing (0: forward; 1: backward) (Default value = 0)

    Returns:
        S_L_final (np.ndarray): Smoothed SM
    """
    N = S.shape[0]
    M = S.shape[1]
    num = len(tempo_rel_set)
    S_L_final = np.zeros((N, M))

    for s in range(0, num):
        M_ceil = int(np.ceil(M / tempo_rel_set[s]))
        resample = np.multiply(np.divide(np.arange(1, M_ceil+1), M_ceil), M)
        np.around(resample, 0, resample)
        resample = resample - 1
        index_resample = np.maximum(resample, np.zeros(len(resample))).astype(np.int64)
        S_resample = S[:, index_resample]

        S_L = np.zeros((N, M_ceil))
        S_extend_L = np.zeros((N + L, M_ceil + L))

        # Forward direction
        if direction == 0:
            S_extend_L[0:N, 0:M_ceil] = S_resample
            for pos in range(0, L):
                S_L = S_L + S_extend_L[pos:(N + pos), pos:(M_ceil + pos)]

        # Backward direction
        if direction == 1:
            S_extend_L[L:(N+L), L:(M_ceil+L)] = S_resample
            for pos in range(0, L):
                S_L = S_L + S_extend_L[(L-pos):(N + L - pos), (L-pos):(M_ceil + L - pos)]

        S_L = S_L / L
        resample = np.multiply(np.divide(np.arange(1, M+1), M), M_ceil)
        np.around(resample, 0, resample)
        resample = resample - 1
        index_resample = np.maximum(resample, np.zeros(len(resample))).astype(np.int64)

        S_resample_inv = S_L[:, index_resample]
        S_L_final = np.maximum(S_L_final, S_resample_inv)

    return S_L_final
def compute_tempo_rel_set(tempo_rel_min, tempo_rel_max, num):
    """Compute logarithmically spaced relative tempo values

    Notebook: C4/C4S2_SSM-PathEnhancement.ipynb

    Args:
        tempo_rel_min (float): Minimum relative tempo
        tempo_rel_max (float): Maximum relative tempo
        num (int): Number of relative tempo values (inlcuding the min and max)

    Returns:
        tempo_rel_set (np.ndarray): Set of relative tempo values
    """
    tempo_rel_set = np.exp(np.linspace(np.log(tempo_rel_min), np.log(tempo_rel_max), num))
    return tempo_rel_set
def threshold_matrix(S, thresh, strategy='absolute', scale=False, penalty=0.0, binarize=False):
    """Treshold matrix in a relative fashion

    Notebook: C4/C4S2_SSM-Thresholding.ipynb

    Args:
        S (np.ndarray): Input matrix
        thresh (float or list): Treshold (meaning depends on strategy)
        strategy (str): Thresholding strategy ('absolute', 'relative', 'local') (Default value = 'absolute')
        scale (bool): If scale=True, then scaling of positive values to range [0,1] (Default value = False)
        penalty (float): Set values below treshold to value specified (Default value = 0.0)
        binarize (bool): Binarizes final matrix (positive: 1; otherwise: 0) (Default value = False)

    Returns:
        S_thresh (np.ndarray): Thresholded matrix
    """
    if np.min(S) < 0:
        raise Exception('All entries of the input matrix must be nonnegative')

    S_thresh = np.copy(S)
    N, M = S.shape
    num_cells = N * M

    if strategy == 'absolute':
        thresh_abs = thresh
        S_thresh[S_thresh < thresh] = 0

    if strategy == 'relative':
        thresh_rel = thresh
        num_cells_below_thresh = int(np.round(S_thresh.size*(1-thresh_rel)))
        if num_cells_below_thresh < num_cells:
            values_sorted = np.sort(S_thresh.flatten('F'))
            thresh_abs = values_sorted[num_cells_below_thresh]
            S_thresh[S_thresh < thresh_abs] = 0
        else:
            S_thresh = np.zeros([N, M])

    if strategy == 'local':
        thresh_rel_row = thresh[0]
        thresh_rel_col = thresh[1]
        S_binary_row = np.zeros([N, M])
        num_cells_row_below_thresh = int(np.round(M * (1-thresh_rel_row)))
        for n in range(N):
            row = S[n, :]
            values_sorted = np.sort(row)
            if num_cells_row_below_thresh < M:
                thresh_abs = values_sorted[num_cells_row_below_thresh]
                S_binary_row[n, :] = (row >= thresh_abs)
        S_binary_col = np.zeros([N, M])
        num_cells_col_below_thresh = int(np.round(N * (1-thresh_rel_col)))
        for m in range(M):
            col = S[:, m]
            values_sorted = np.sort(col)
            if num_cells_col_below_thresh < N:
                thresh_abs = values_sorted[num_cells_col_below_thresh]
                S_binary_col[:, m] = (col >= thresh_abs)
        S_thresh = S * S_binary_row * S_binary_col

    if scale:
        cell_val_zero = np.where(S_thresh == 0)
        cell_val_pos = np.where(S_thresh > 0)
        if len(cell_val_pos[0]) == 0:
            min_value = 0
        else:
            min_value = np.min(S_thresh[cell_val_pos])
        max_value = np.max(S_thresh)
        # print('min_value = ', min_value, ', max_value = ', max_value)
        if max_value > min_value:
            S_thresh = np.divide((S_thresh - min_value), (max_value - min_value))
            if len(cell_val_zero[0]) > 0:
                S_thresh[cell_val_zero] = penalty
        else:
            print('Condition max_value > min_value is voliated: output zero matrix')

    if binarize:
        S_thresh[S_thresh > 0] = 1
        S_thresh[S_thresh < 0] = 0
    return S_thresh

def normalize_ssm(S):
    """Normalizes self-similartiy matrix to fulfill S(n,n)=1.
    Yields a warning if max(S)<=1 is not fulfilled

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        S (np.ndarray): Self-similarity matrix (SSM)

    Returns:
        S_normalized (np.ndarray): Normalized self-similarity matrix
    """
    S_normalized = S.copy()
    N = S_normalized.shape[0]
    for n in range(N):
        S_normalized[n, n] = 1
        max_S = np.max(S_normalized)
    if max_S > 1:
        print('Normalization condition for SSM not fulfill (max > 1)')
    return S_normalized
# -------- [ TRANSPOSE ] -------

def shift_cyc_matrix(X, shift=0):
    """Cyclic shift of features matrix along first dimension

    Notebook: C4/C4S2_SSM-TranspositionInvariance.ipynb

    Args:
        X (np.ndarray): Feature respresentation
        shift (int): Number of bins to be shifted (Default value = 0)

    Returns:
        X_cyc (np.ndarray): Cyclically shifted feature matrix
    """
    # Note: X_cyc = np.roll(X, shift=shift, axis=0) does to work for jit
    K, N = X.shape
    shift = np.mod(shift, K)
    X_cyc = np.zeros((K, N))
    X_cyc[shift:K, :] = X[0:K-shift, :]
    X_cyc[0:shift, :] = X[K-shift:K, :]
    return X_cyc
def compute_sm_ti(X, Y, L=1, tempo_rel_set=np.asarray([1]), shift_set=np.asarray([0]), direction=2):
    """Compute enhanced similaity matrix by applying path smoothing and transpositions

    Notebook: C4/C4S2_SSM-TranspositionInvariance.ipynb

    Args:
        X (np.ndarray): First feature sequence
        Y (np.ndarray): Second feature sequence
        L (int): Length of filter (Default value = 1)
        tempo_rel_set (np.ndarray): Set of relative tempo values (Default value = np.asarray([1]))
        shift_set (np.ndarray): Set of shift indices (Default value = np.asarray([0]))
        direction (int): Direction of smoothing (0: forward; 1: backward; 2: both directions) (Default value = 2)

    Returns:
        S_TI (np.ndarray): Transposition-invariant SM
        I_TI (np.ndarray): Transposition index matrix
    """
    for shift in shift_set:
        Y_cyc = shift_cyc_matrix(Y, shift)
        S_cyc = libfmp.c4.compute_sm_dot(X, Y_cyc)

        if direction == 0:
            S_cyc = libfmp.c4.filter_diag_mult_sm(S_cyc, L, tempo_rel_set, direction=0)
        if direction == 1:
            S_cyc = libfmp.c4.filter_diag_mult_sm(S_cyc, L, tempo_rel_set, direction=1)
        if direction == 2:
            S_forward = libfmp.c4.filter_diag_mult_sm(S_cyc, L, tempo_rel_set=tempo_rel_set, direction=0)
            S_backward = libfmp.c4.filter_diag_mult_sm(S_cyc, L, tempo_rel_set=tempo_rel_set, direction=1)
            S_cyc = np.maximum(S_forward, S_backward)
        if shift == shift_set[0]:
            S_TI = S_cyc
            I_TI = np.ones((S_cyc.shape[0], S_cyc.shape[1])) * shift
        else:
            # jit does not like the following lines
            # I_greater = np.greater(S_cyc, S_TI)
            # I_greater = (S_cyc > S_TI)
            I_TI[S_cyc > S_TI] = shift
            S_TI = np.maximum(S_cyc, S_TI)

    return S_TI, I_TI

# -------- [ SCORE ] --------
def compute_fitness(path_family, score, N):
    """Compute fitness measure and other metrics from path family

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        path_family (list): Path family
        score (float): Score
        N (int): Length of feature sequence

    Returns:
        fitness (float): Fitness
        score (float): Score
        score_n (float): Normalized score
        coverage (float): Coverage
        coverage_n (float): Normalized coverage
        path_family_length (int): Length of path family (total number of cells)
    """
    eps = 1e-16
    num_path = len(path_family)
    M = path_family[0][-1][1] + 1

    # Normalized score
    path_family_length = 0
    for n in range(num_path):
        path_family_length = path_family_length + len(path_family[n])
    score_n = (score - M) / (path_family_length + eps)

    # Normalized coverage
    segment_family, coverage = compute_induced_segment_family_coverage(path_family)
    coverage_n = (coverage - M) / (N + eps)

    # Fitness measure
    fitness = 2 * score_n * coverage_n / (score_n + coverage_n + eps)

    return fitness, score, score_n, coverage, coverage_n, path_family_length
def compute_induced_segment_family_coverage(path_family):
    """Compute induced segment family and coverage from path family

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        path_family (list): Path family

    Returns:
        segment_family (np.ndarray): Induced segment family
        coverage (float): Coverage of path family
    """
    num_path = len(path_family)
    coverage = 0
    if num_path > 0:
        segment_family = np.zeros((num_path, 2), dtype=int)
        for n in range(num_path):
            segment_family[n, 0] = path_family[n][0][0]
            segment_family[n, 1] = path_family[n][-1][0]
            coverage = coverage + segment_family[n, 1] - segment_family[n, 0] + 1
    else:
        segment_family = np.empty

    return segment_family, coverage
def compute_accumulated_score_matrix(S_seg):
    """Compute the accumulated score matrix

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        S_seg (np.ndarray): Submatrix of an enhanced and normalized SSM ``S``.
            Note: ``S`` must satisfy ``S(n,m) <= 1 and S(n,n) = 1``

    Returns:
        D (np.ndarray): Accumulated score matrix
        score (float): Score of optimal path family
    """
    inf = math.inf
    N = S_seg.shape[0]
    M = S_seg.shape[1]+1

    # Iinitializing score matrix
    D = -inf * np.ones((N, M), dtype=np.float64)
    D[0, 0] = 0.
    D[0, 1] = D[0, 0] + S_seg[0, 0]

    # Dynamic programming
    for n in range(1, N):
        D[n, 0] = max(D[n-1, 0], D[n-1, -1])
        D[n, 1] = D[n, 0] + S_seg[n, 0]
        for m in range(2, M):
            D[n, m] = S_seg[n, m-1] + max(D[n-1, m-1], D[n-1, m-2], D[n-2, m-1])

    # Score of optimal path family
    score = np.maximum(D[N-1, 0], D[N-1, M-1])

    return D, score
def compute_optimal_path_family(D):
    """Compute an optimal path family given an accumulated score matrix

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        D (np.ndarray): Accumulated score matrix

    Returns:
        path_family (list): Optimal path family consisting of list of paths
            (each path being a list of index pairs)
    """
    # Initialization
    inf = math.inf
    N = int(D.shape[0])
    M = int(D.shape[1])

    path_family = []
    path = []

    n = N - 1
    if(D[n, M-1] < D[n, 0]):
        m = 0
    else:
        m = M-1
        path_point = (N-1, M-2)
        path.append(path_point)

    # Backtracking
    while n > 0 or m > 0:

        # obtaining the set of possible predecesors given our current position
        if(n <= 2 and m <= 2):
            predecessors = [(n-1, m-1)]
        elif(n <= 2 and m > 2):
            predecessors = [(n-1, m-1), (n-1, m-2)]
        elif(n > 2 and m <= 2):
            predecessors = [(n-1, m-1), (n-2, m-1)]
        else:
            predecessors = [(n-1, m-1), (n-2, m-1), (n-1, m-2)]

        # case for the first row. Only horizontal movements allowed
        if n == 0:
            cell = (0, m-1)
        # case for the elevator column: we can keep going down the column or jumping to the end of the next row
        elif m == 0:
            if D[n-1, M-1] > D[n-1, 0]:
                cell = (n-1, M-1)
                path_point = (n-1, M-2)
                if(len(path) > 0):
                    path.reverse()
                    path_family.append(path)
                path = [path_point]
            else:
                cell = (n-1, 0)
        # case for m=1, only horizontal steps to the elevator column are allowed
        elif m == 1:
            cell = (n, 0)
        # regular case
        else:

            # obtaining the best of the possible predecesors
            max_val = -inf
            for i, cur_predecessor in enumerate(predecessors):
                if(max_val < D[cur_predecessor[0], cur_predecessor[1]]):
                    max_val = D[cur_predecessor[0], cur_predecessor[1]]
                    cell = cur_predecessor

            # saving the point in the current path
            path_point = (cell[0], cell[1]-1)
            path.append(path_point)

        (n, m) = cell

    # adding last path to the path family
    path.reverse()
    path_family.append(path)
    path_family.reverse()

    return path_family


# -------- [ PLOT ] --------
def plot_ssm_ann(S, Fs=1, cmap='gray_r', figsize=(5, 4.5), xlabel='', ylabel='', title=''):
    """Plot SSM and annotations (horizontal and vertical as overlay)

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        S: Self-similarity matrix
        ann: Annotations
        Fs: Feature rate of path_family (Default value = 1)
        cmap: Color map for S (Default value = 'gray_r')
        color_ann: color scheme used for annotations (see :func:`libfmp.b.b_plot.plot_segments`)
            (Default value = [])
        ann_x: Plot annotations on x-axis (Default value = True)
        ann_y: Plot annotations on y-axis (Default value = True)
        fontsize: Font size used for annotation labels (Default value = 12)
        figsize: Size of figure (Default value = (5, 4.5))
        xlabel: Label for x-axis (Default value = '')
        ylabel: Label for y-axis (Default value = '')
        title: Figure size (Default value = '')

    Returns:
        fig: Handle for figure
        ax: Handle for axes
        im: Handle for imshow
    """
    fig, ax = plt.subplots(2, 2, gridspec_kw={'width_ratios': [1, 0.05],
                                              'height_ratios': [1, 0.1]}, figsize=figsize)

    fig_im, ax_im, im = libfmp.b.plot_matrix(S, Fs=Fs, Fs_F=Fs,
                                             ax=[ax[0, 0], ax[0, 1]], cmap=cmap,
                                             xlabel='', ylabel='', title='')
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].set_xlabel(xlabel)
    ax[0, 0].set_title(title)
    plt.tight_layout()
    return fig, ax, im

def plot_path_family(ax, path_family, Fs=1, x_offset=0, y_offset=0, proj_x=True, w_x=7, proj_y=True, w_y=7):
    """Plot path family into a given axis

    Notebook: C4/C4S3_AudioThumbnailing.ipynb

    Args:
        ax: Axis of plot
        path_family: Path family
        Fs: Feature rate of path_family (Default value = 1)
        x_offset: Offset x-axis (Default value = 0)
        y_offset: Yffset x-axis (Default value = 0)
        proj_x: Display projection on x-axis (Default value = True)
        w_x: Width used for projection on x-axis (Default value = 7)
        proj_y: Display projection on y-axis (Default value = True)
        w_y: Width used for projection on y-axis (Default value = 7)
    """
    for path in path_family:
        y = [(path[i][0] + y_offset)/Fs for i in range(len(path))]
        x = [(path[i][1] + x_offset)/Fs for i in range(len(path))]
        ax.plot(x, y, "o", color=[0, 0, 0], linewidth=3, markersize=5)
        ax.plot(x, y, '.', color=[0.7, 1, 1], linewidth=2, markersize=6)
    if proj_y:
        for path in path_family:
            y1 = path[0][0]/Fs
            y2 = path[-1][0]/Fs
            ax.add_patch(plt.Rectangle((0, y1), w_y, y2-y1, linewidth=1,
                                       facecolor=[0, 1, 0], edgecolor=[0, 0, 0]))
            # ax.plot([0, 0], [y1, y2], linewidth=8, color=[0, 1, 0])
    if proj_x:
        for path in path_family:
            x1 = (path[0][1] + x_offset)/Fs
            x2 = (path[-1][1] + x_offset)/Fs
            ax.add_patch(plt.Rectangle((x1, 0), x2-x1, w_x, linewidth=1,
                                       facecolor=[0, 0, 1], edgecolor=[0, 0, 0]))


def detectStructure(path):
    # X = feature.extract_feature(path,"chroma_cqt")
    Fs = 22050
    Hop_len = 2205
    x, Fs = librosa.load(path, sr=Fs)

    print(f"wave len:{len(x)}")
    X = librosa.feature.chroma_stft(y=x, sr=Fs, tuning=0, norm=2, hop_length=Hop_len, n_fft=4410)
    print(f"chroma len:{X.shape[1]}")

    # Chroma Feature Sequence and SSM (10 Hz)
    L, H = 41, 10
    Fs_C = Fs / Hop_len
    X, Fs_feature = smooth_downsample_feature_sequence(X, Fs_C, filt_len=L, down_sampling=H)
    X = normalize_feature_sequence(X, norm='2', threshold=0.001)

    SSM = np.dot(X.T, X)

    # Normalize SSM
    SSM = normalize_ssm(SSM)
    SSM_NORM = SSM

    # SSM Enhancement
    SSM = filter_diag_sm(SSM, 10)

    # SSM Transpose
    tempo_rel_set = libfmp.c4.compute_tempo_rel_set(0.66, 1.5, 5)
    shift_set = np.array(range(12))
    SSM, I_TI = compute_sm_ti(X, X, L=8, tempo_rel_set=tempo_rel_set, shift_set=shift_set, direction=2)

    # SSM: Thresholding
    # SSM, I_TI = libfmp.c4.compute_sm_ti(X, X, L=8, tempo_rel_set=tempo_rel_set, shift_set=shift_set, direction=2)
    SSM = threshold_matrix(SSM, thresh=0.15, strategy='relative', penalty=-2, scale=True)

    # Audio Thumbnailing (Segment Matching & Path Packing)
    seg_sec = [25, 73]
    seg = [int(seg_sec[0] * Fs_feature), int(seg_sec[1] * Fs_feature)]
    N = SSM.shape[0]
    S_seg = SSM[:, seg[0]:seg[1] + 1]

    D, score = compute_accumulated_score_matrix(S_seg)
    path_family = compute_optimal_path_family(D)


    # fitness, score, score_n, coverage, coverage_n, path_family_length = compute_fitness(path_family, score, N)


    print(path_family)
    # Finally Grouping segments into familty
    segment_family, coverage = compute_induced_segment_family_coverage(path_family)

    for segment in segment_family:
        print(f"{segment[0]}\t{segment[1]}")
        t_start = str(datetime.timedelta(seconds=int(segment[0])))
        t_end = str(datetime.timedelta(seconds=int(segment[1])))
        print(f"{t_start}\t{t_end}")

    # Novety Decection (Strcuture Boundary Detection)
    nov = compute_novelty_ssm(SSM_NORM, L=20, exclude=True)
    # peaks = peak_picking_simple(nov)
    # wait = 10
    # peaks = librosa.util.peak_pick(nov, pre_max=5, post_max=5, pre_avg=5, post_avg=5,
    #                                delta=0.01, wait=wait)
    peaks, nov_norm, threshold_local = peak_picking_MSAF(nov)

    output = {
        "segments":segment_family,
        "boundaries":peaks
    }

    return output



# if __name__ == '__main__':
#     path = "/Users/nurupo/Desktop/dev/audio/test/donki2.mp3"
#     #X = feature.extract_feature(path,"chroma_cqt")
#     Fs = 22050
#     Hop_len = 2205
#     x, Fs = librosa.load(path, sr=Fs)
#
#     print(f"wave len:{len(x)}")
#     X = librosa.feature.chroma_stft(y=x, sr=Fs, tuning=0, norm=2, hop_length=Hop_len, n_fft=4410)
#     print(f"chroma len:{X.shape[1]}")
#
#
#     # Chroma Feature Sequence and SSM (10 Hz)
#     L, H = 41, 10
#     Fs_C = Fs / Hop_len
#     X,Fs_feature = smooth_downsample_feature_sequence(X, Fs_C, filt_len=L, down_sampling=H)
#     X = normalize_feature_sequence(X, norm='2', threshold=0.001)
#
#
#     SSM = np.dot(X.T, X)
#
#     # Normalize SSM
#     SSM = normalize_ssm(SSM)
#     SSM_NORM = SSM
#
#     # SSM Enhancement
#     SSM = filter_diag_sm(SSM,10)
#
#
#
#     # SSM Transpose
#     tempo_rel_set = libfmp.c4.compute_tempo_rel_set(0.66, 1.5, 5)
#     shift_set = np.array(range(12))
#     SSM, I_TI = compute_sm_ti(X, X, L=8, tempo_rel_set=tempo_rel_set, shift_set=shift_set, direction=2)
#
#
#
#     # SSM: Thresholding
#     #SSM, I_TI = libfmp.c4.compute_sm_ti(X, X, L=8, tempo_rel_set=tempo_rel_set, shift_set=shift_set, direction=2)
#     SSM = threshold_matrix(SSM, thresh=0.15, strategy='relative',penalty=-2,scale=True)
#
#
#
#     # Audio Thumbnailing (Segment Matching & Path Packing)
#     seg_sec = [96,136]
#     seg = [int(seg_sec[0] * Fs_feature), int(seg_sec[1] * Fs_feature)]
#     N = SSM.shape[0]
#     S_seg = SSM[:, seg[0]:seg[1] + 1]
#
#     D, score = compute_accumulated_score_matrix(S_seg)
#     path_family = compute_optimal_path_family(D)
#
#     plt.figure(figsize=(5, 5))
#     sns.heatmap(D, cmap="gray_r", cbar=False)
#     plt.gca().invert_yaxis()  # This inverts the y-axis
#     plt.tight_layout()
#     plt.show()
#     #fitness, score, score_n, coverage, coverage_n, path_family_length = compute_fitness(path_family, score, N)
#
#     fig, ax, im = plot_ssm_ann(SSM,Fs=Fs_feature, xlabel=r'$\alpha=[%d:%d]$' % (seg[0], seg[-1]))
#     plot_path_family(ax[0, 0], path_family, Fs=Fs_feature, x_offset=seg[0])
#     plt.show()
#     print(path_family)
#     # Finally Grouping segments into familty
#     segment_family, coverage = compute_induced_segment_family_coverage(path_family)
#
#
#
#     for segment in segment_family:
#         print(f"{segment[0]}\t{segment[1]}")
#         t_start = str(datetime.timedelta(seconds=int(segment[0])))
#         t_end = str(datetime.timedelta(seconds=int(segment[1])))
#         print(f"{t_start}\t{t_end}")
#
#
#
#     # Novety Decection (Strcuture Boundary Detection)
#     nov = compute_novelty_ssm(SSM_NORM, L=20, exclude=True)
#     #peaks = peak_picking_simple(nov)
#     # wait = 10
#     # peaks = librosa.util.peak_pick(nov, pre_max=5, post_max=5, pre_avg=5, post_avg=5,
#     #                                delta=0.01, wait=wait)
#     peaks,nov_norm,threshold_local = peak_picking_MSAF(nov)
#
#
#
#     sns.lineplot(nov,color="grey")
#     sns.lineplot(nov_norm,color="magenta")
#     sns.lineplot(threshold_local,color="blue")
#     for peak in peaks:
#         plt.axvline(x=peak, color='red', linestyle='--')
#     plt.show()
#
#     #sns.set(rc={'figure.figsize': (15, 5)})
#     sns.heatmap(SSM,cmap="gray_r")
#     for peak in peaks:
#         plt.axvline(x=peak, color='red', linestyle='--')
#         plt.axhline(y=peak, color='red', linestyle='--')
#
#     plt.gca().invert_yaxis()  # This inverts the y-axis
#     plt.tight_layout()
#     plt.show()