import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load an audio file
y, sr = librosa.load('./vocal_reb.wav')

# Compute the Mel-spectrogram
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

# Apply PCEN to the Mel-spectrogram
S_pcen = librosa.pcen(S, sr=sr)

# Normalize the PCEN spectrogram
#S_pcen_norm = librosa.util.normalize(S_pcen, axis=1)

# Create a figure with two subplots
fig, axs = plt.subplots(nrows=2, sharex=True)

# Plot the Mel-spectrogram on the first subplot
librosa.display.specshow(librosa.power_to_db(S, ref=np.max), ax=axs[0],y_axis='mel', x_axis='time')

# Set the title and y-label of the first subplot
axs[0].set(title='Mel-Spectrogram', ylabel='Hz')

# Plot the PCEN spectrogram on the second subplot
librosa.display.specshow(librosa.power_to_db(S_pcen, ref=np.max), ax=axs[1],y_axis='mel', x_axis='time')

# Set the title and y-label of the second subplot
axs[1].set(title='PCEN Spectrogram', ylabel='Hz')

# Add a shared x-label to the bottom subplot
plt.xlabel('Time (s)')

# Add a colorbar to the plot
plt.colorbar(format='%+2.0f dB')

# Adjust the layout and display the figure
fig.tight_layout()
plt.show()
