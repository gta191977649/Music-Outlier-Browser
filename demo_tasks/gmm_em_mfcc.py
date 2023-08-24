import librosa
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Load audio file
y, sr = librosa.load("../demo.wav", sr=None)

# Extract MFCCs
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)
print()
# Fit GMM
gmm_components = 3
gmm = GaussianMixture(n_components=gmm_components)  # You can choose the number of components
gmm.fit(mfccs.T)  # The input should be transposed to have frames as rows

# Get GMM parameters
means = gmm.means_
covariances = gmm.covariances_
weights = gmm.weights_

# Create a plot
plt.figure(figsize=(10, 6))
mfcc_indices = np.arange(1, 13)

for i in range(gmm_components):
    plt.plot(mfcc_indices, means[i], label=f'Component {i + 1}', linewidth=2)
    plt.fill_between(mfcc_indices, means[i] - np.sqrt(covariances[i].diagonal()),
                     means[i] + np.sqrt(covariances[i].diagonal()), alpha=0.3)

plt.xlabel('MFCC Index')
plt.ylabel('MFCC Value')
plt.legend()
plt.title('GMM Components fitted to 12-dimensional MFCC vectors')
plt.show()
