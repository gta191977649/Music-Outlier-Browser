import librosa
import numpy as np
import matplotlib.pyplot as plt

def compute_residuals(y, order=16):
    """Compute the LPC residuals for a given audio signal."""
    a = librosa.lpc(y, order=order)
    y_hat = np.convolve(y, a)[:len(y)]
    residuals = y - y_hat
    return residuals
def normalize_signal(signal):
    """Normalize a signal to the range [-1, 1]."""
    return signal / np.max(np.abs(signal))

# Load the audio file
y, sr = librosa.load("../demo.wav", sr=None)

# Compute LPC residuals for the entire audio
residuals = compute_residuals(y)

# Compute chroma features for the entire audio
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# Normalize the audio signal and residuals
y_normalized = normalize_signal(y)
residuals_normalized = normalize_signal(residuals)

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(12, 10))

# Plot original waveform and residuals
axs[0].plot(y_normalized, label='Normalized Waveform', alpha=1,color='blue')
axs[0].plot(residuals_normalized, label='Normalized LPC Residuals', alpha=0.2, color='red')
axs[0].set_ylabel('Amplitude')
axs[0].set_title('Original Waveform vs. LPC Residuals')
axs[0].set_xlim(0, len(y))
axs[0].legend()
axs[0].grid(True)

# Plot chroma
chroma_img = axs[1].imshow(chroma, aspect='auto', origin='lower', cmap='viridis', extent=[0, len(y), 0, 12])
axs[1].set_ylabel('Pitch Class')
axs[1].set_yticks(np.arange(12))
axs[1].set_yticklabels(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
axs[1].set_xlabel('Sample Index')
axs[1].set_title('Chroma Features')

plt.tight_layout()
plt.savefig("lpc_chroma.png")
plt.show()
