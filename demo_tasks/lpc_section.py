import librosa
import numpy as np
import matplotlib.pyplot as plt

def compute_residuals(y, order=16):
    """Compute the LPC residuals for a given audio signal."""
    # Compute the LPC coefficients
    a = librosa.lpc(y, order=order)
    # Use the coefficients to predict the signal
    y_hat = np.convolve(y, a)
    # Calculate the residuals
    residuals = y - y_hat[:len(y)]
    return residuals

# Load the audio file
y, sr = librosa.load("../demo.wav")

# Segment the song into fixed-length segments
segment_length = sr * 1  # 10 seconds for this example
segments = [y[i:i+segment_length] for i in range(0, len(y), segment_length)]

# Compute LPC residuals for each segment
residuals = [np.mean(np.abs(compute_residuals(seg))) for seg in segments]

# Compute average chroma for each segment
chroma_features = [np.mean(librosa.feature.chroma_stft(y=seg, sr=sr), axis=1) for seg in segments]

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# Plot residuals
axs[0].plot(residuals)
axs[0].set_ylabel('Mean Absolute Residual')
axs[0].set_title('LPC Residuals for Song Segments')
axs[0].grid(True)
axs[0].set_xlim(0, len(segments)-1)

# Plot chroma
chroma_img = axs[1].imshow(np.array(chroma_features).T, aspect='auto', origin='lower', cmap='viridis')
axs[1].set_ylabel('Pitch Class')
axs[1].set_yticks(np.arange(12))
axs[1].set_yticklabels(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
axs[1].set_xlabel('Segment Index')
axs[1].set_title('Chroma Features for Song Segments')
axs[1].set_xlim(0, len(segments)-1)

plt.tight_layout()
plt.show()
