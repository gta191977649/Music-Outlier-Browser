# This script provides verious of different type feature extration funciton
import librosa
import numpy as np
from gammatone import fftweight
from scipy import interpolate


def dspFilterBank(filterBank, y, sr):
    n_fft = 2048
    hop_length = 512
    win_length = n_fft  # Assuming win_length is the same as n_fft
    window = 'hann'  # Assuming the Gammatone filter bank accepts the same window types

    if filterBank == "mel":
        # Use built in librosa mel-filter bank
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length,
                                                         win_length=win_length, window=window)
        return mel_spectrogram
    if filterBank == "gamma":
        gammatone_spectrogram = fftweight.fft_gtgram(y, sr, window_time=win_length / sr, hop_time=hop_length / sr,
                                                     channels=128, f_min=0)
        """
        Compute Gammatone spectrogram using fft_gtgram function 
        Parameters:
        y:  Audio signal, should be a 1-D numpy array.
        sr: Sampling rate of the audio signal.
        window_time: Duration of each window for short-time Fourier transform (STFT), in seconds. 
                     A value of 0.025s (25 milliseconds) is typical and provides a good trade-off 
                     between time and frequency resolution.
        hop_time: Step size or hop length between successive windows, in seconds.
                  A value of 0.010s (10 milliseconds) is typical and provides a good overlap between windows 
                  for smoother spectral representations.
        channels: Number of filter channels in the Gammatone filter bank.
                  A value of 20 is chosen as a common configuration for audio analysis tasks, 
                  but this can be adjusted based on the requirements of your application.
        f_min: Minimum frequency to consider in the filter bank, in Hz.
               A value of 50 Hz is chosen to include low-frequency content while excluding 
               frequencies that are typically outside the range of human hearing.
        """
        return gammatone_spectrogram


def extractFeature(y, sr, type="rms", filterBank="mel"):
    """
    y: signal in time-domain
    sr: sample rate of source audio file
    """
    n_fft = 2048
    hop_length = 512
    # Calculate the desired number of frames based on the audio length and hop_length
    desired_num_frames = 1 + (len(y) - n_fft) // hop_length

    if type == "loudness":
        # deal with whatever filter banks want to use
        spectrogram = dspFilterBank(filterBank=filterBank, y=y, sr=sr)
        # Compute loudness
        loudness = np.sum(spectrogram, axis=0)
        if filterBank == "gamma":
            loudness = loudness ** 2
        loudness_db = librosa.power_to_db(loudness)
        # Adjust the loudness values to a negative dB scale
        loudness_db -= np.max(loudness_db)  # Subtract the maximum loudness value from all loudness values

        # Standardize the frame length by interpolating the loudness array
        if len(loudness_db) != desired_num_frames:
            x_old = np.linspace(0, 1, len(loudness_db))
            x_new = np.linspace(0, 1, desired_num_frames)
            interpolator = interpolate.interp1d(x_old, loudness_db, kind='linear', fill_value='extrapolate')
            loudness_db = interpolator(x_new)

        return loudness_db
    if type == "rms":
        rms = librosa.feature.rms(y=y)
        return rms