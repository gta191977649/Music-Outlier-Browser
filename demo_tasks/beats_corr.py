import librosa
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# Function to extract a feature (adjustable)
def extract_feature(segment, feature_type='amplitude', sr=22050):
    if feature_type == 'amplitude':
        return np.mean(np.abs(segment))
    elif feature_type == 'chroma':
        chroma = librosa.feature.chroma_stft(y=segment, sr=sr)
        return np.mean(chroma, axis=1)  # Averaging across all frames
    else:
        return None


# Load audio file
y, sr = librosa.load('../music/nogizaka_demo.wav',duration=30)

# Beat detection
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

# Define the segment length in milliseconds
segment_length_ms = 25  # 25 milliseconds

# Convert segment length to number of samples
segment_length_samples = int(segment_length_ms * sr / 1000)

# Feature extraction for each beat
feature_type = 'amplitude'  # Change this to extract different features
beat_features = []
for beat in beats:
    start = max(0, beat - segment_length_samples)
    end = min(len(y), beat + segment_length_samples)
    segment = y[start:end]

    # Extract the chosen feature
    feature_value = extract_feature(segment, feature_type, sr)
    beat_features.append(feature_value)

# Convert to NumPy array
beat_features_array = np.array(beat_features)

# If feature is chroma, it will be 2D; we can use mean or other statistics for simplification
if feature_type == 'chroma':
    beat_features_array = np.mean(beat_features_array, axis=1)

# Min-Max normalization
min_val = np.min(beat_features_array)
max_val = np.max(beat_features_array)
beat_features_array = (beat_features_array - min_val) / (max_val - min_val)

# Calculate the Euclidean distance between each pair of feature values
distance_matrix = squareform(pdist(beat_features_array.reshape(-1, 1), 'euclidean'))

# Create a larger figure
plt.figure(figsize=(15, 15))

# Plot the distance matrix
sns.heatmap(distance_matrix, annot=False, cmap='coolwarm')
plt.title(f'Euclidean Distance Between Beats Using {feature_type.capitalize()}')
plt.xlabel('Beat Index')
plt.ylabel('Beat Index')

# Show the plot
plt.show()
