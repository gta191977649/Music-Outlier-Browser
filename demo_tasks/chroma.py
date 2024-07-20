import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def draw_spectrogram_and_chromagram(mp3_path):
    # Load the audio file with a specific sample rate
    y, sr = librosa.load(mp3_path, sr=11000)

    # Compute the Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y)
    db_stft = librosa.amplitude_to_db(abs(stft))

    # Compute the Constant-Q Transform chromagram
    chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)
    # Apply temporal smoothing
    chromagram = librosa.decompose.nn_filter(chromagram, aggregate=np.median, metric='cosine')
    # Normalize the chromagram
    chromagram = librosa.util.normalize(chromagram)

    # Create a figure to host the plots
    plt.figure(figsize=(20, 8))

    # Plot STFT spectrogram
    plt.subplot(2, 1, 1)  # 2 rows, 1 column, first subplot
    librosa.display.specshow(db_stft, sr=sr, x_axis='time', y_axis='log')
    #plt.colorbar(format='%+2.0f dB')
    plt.title('STFT Spectrogram')

    # Plot chromagram
    plt.subplot(2, 1, 2)  # 2 rows, 1 column, second subplot
    librosa.display.specshow(chromagram, y_axis='chroma', x_axis='time', sr=sr)
    plt.title('CQT Chromagram')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    mp3_file_path = '../music/love_is_in_the_air.mp3'
    draw_spectrogram_and_chromagram(mp3_file_path)
