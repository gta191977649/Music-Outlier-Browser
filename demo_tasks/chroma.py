import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def draw_enhanced_chromagram(mp3_path):
    # Load the MP3 file with a sample rate of 44100
    y, sr = librosa.load(mp3_path, sr=44100)

    # Extract the chromagram
    chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

    # Apply temporal smoothing
    chromagram = librosa.decompose.nn_filter(chromagram, aggregate=np.median, metric='cosine')

    # Normalize
    chromagram = librosa.util.normalize(chromagram)

    # Apply thresholding to make values closer to 0 or 1
    threshold = 0.7
    chromagram = np.where(chromagram > threshold, 1, 0)

    # Plot the chromagram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(chromagram, y_axis='chroma', x_axis='time', sr=sr, cmap='gray_r')
    plt.title('Enhanced Chromagram')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    mp3_file_path = '../test_main.wav'
    draw_enhanced_chromagram(mp3_file_path)