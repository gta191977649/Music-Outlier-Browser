import numpy as np
import librosa
import matplotlib.pyplot as plt

def compute_lpc(y, sr, order=16):
    """Compute LPC coefficients for an audio segment."""
    return librosa.lpc(y, order=order)

def compute_difference(coeffs1, coeffs2):
    """Compute difference between two sets of LPC coefficients."""
    return np.linalg.norm(coeffs1 - coeffs2)

def segment_audio(y, sr, segment_length=0.1):
    """Segment audio into fixed-length windows."""
    samples_per_segment = int(segment_length * sr)
    num_segments = len(y) // samples_per_segment
    return [y[i*samples_per_segment : (i+1)*samples_per_segment] for i in range(num_segments)]

def enhance_data(data, threshold=0.7):
    """Enhance data to make values closer to 0 or 1."""
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
    return np.where(normalized_data > threshold, 1, 0)

def smooth_chroma(chroma, window_size=3):
    """Apply moving average smoothing to chroma features."""
    smoothed_chroma = np.apply_along_axis(lambda m: np.convolve(m, np.ones(window_size)/window_size, mode='valid'), 1, chroma)
    return smoothed_chroma

# Load an audio file
y, sr = librosa.load("./test_main.wav", sr=44100)

# Customize the segment length here
segment_length = 0.06

# Segment audio
segments = segment_audio(y, sr, segment_length)
segment_times = [i * segment_length for i in range(len(segments))]

# Compute LPC coefficients for each segment
coefficients = [compute_lpc(segment, sr) for segment in segments]

# Compute difference between successive segments
differences = [compute_difference(coefficients[i], coefficients[i+1]) for i in range(len(coefficients)-1)]

# Compute chroma_cqt for each segment and average the chroma values within segments
segment_chromagrams = [librosa.feature.chroma_stft(y=segment, sr=sr) for segment in segments]

# Smooth the chroma
smoothed_chromagrams = [smooth_chroma(chroma) for chroma in segment_chromagrams]
segment_chroma_means = [np.mean(chromagram, axis=1) for chromagram in smoothed_chromagrams]

enhanced_chroma_means = [enhance_data(chroma_mean, threshold=0.8) for chroma_mean in segment_chroma_means]

# Plotting the LPC differences and enhanced chromagram against time
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

ax[0].plot(segment_times[:-1], differences)  # We're plotting against segment start times
ax[0].set_xlim(0, segment_times[-1])
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Difference')
ax[0].set_title('LPC')

img = ax[1].imshow(np.array(enhanced_chroma_means).T, aspect='auto', origin='lower', cmap='gray_r', extent=[0, segment_times[-1], 0, 12])
ax[1].set_title('Chroma')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Chroma')

plt.tight_layout()
plt.show()
