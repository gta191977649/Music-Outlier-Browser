# This script provides verious of different type feature extration funciton
# and related DSP operations
import librosa
import numpy as np
from gammatone import fftweight
from scipy import interpolate
import allin1
from config import CONF
import matplotlib.pyplot as plt


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
        NOTE: It returns spectrogram in MAGNITUDE!!!! 
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


def dspEmbeddingSectonFeature(sr, sections, feature):
    hop_length = 512
    for section in sections:
        start_time, end_time = section["time"]
        # Convert time to frames
        start_frame = librosa.time_to_frames(start_time, sr=sr, hop_length=hop_length)
        end_frame = librosa.time_to_frames(end_time, sr=sr, hop_length=hop_length)
        # Extract the features for this section
        section["feature"] = feature[start_frame:end_frame]
    return sections


def extractFeature(y, sr, type="loudness", filterBank="mel", normalize=False):
    """
    y: signal in time-domain
    sr: sample rate of source audio file
    """
    output_feature = []
    n_fft = 2048
    hop_length = 512
    # Calculate the desired number of frames based on the audio length and hop_length
    desired_num_frames = 1 + (len(y) - n_fft) // hop_length
    # 1. deal with whatever filter banks want to use
    # Note dspFilterBank returned the spectrogram in powered
    spectrogram = dspFilterBank(filterBank=filterBank, y=y, sr=sr)

    if type == "loudness":
        # Compute loudness
        loudness = np.sum(spectrogram, axis=0)
        if filterBank == "gamma":
            loudness = loudness ** 2
        output_feature = librosa.power_to_db(loudness)
        # Adjust the loudness values to a negative dB scale
        # Subtract the maximum loudness value from all loudness values
        output_feature -= np.max(output_feature)

    if type == "rms":
        # converts power spectrogram to magnitude if using mel-filterbank
        # the gammatone filter don't need to anything as it already represent in magnitude squared.
        if filterBank == "mel":
            spectrogram = np.sqrt(spectrogram)  # Convert to magnitude spectrogram if necessary
            # Manually compute RMS for each frame
        output_feature = np.sqrt(np.mean(spectrogram ** 2, axis=0))

    if type == "sc":  # Spectral Centroid
        # converts power spectrogram to magnitude if using mel-filterbank
        # the gammatone filter don't need to anything as it already represent in magnitude squared.
        if filterBank == "mel":
            spectrogram = np.sqrt(spectrogram)
        output_feature = librosa.feature.spectral_centroid(S=spectrogram.T, n_fft=n_fft, hop_length=hop_length)[0]

    if type == "zcr":
        # Compute zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y, frame_length=n_fft, hop_length=hop_length)[0]
        # since zcr compute on time domain, there no need for interpolating by the frame level
        return zcr
    # Last Standardize the frame length by interpolating the features array
    if len(output_feature) != desired_num_frames:
        x_old = np.linspace(0, 1, len(output_feature))
        x_new = np.linspace(0, 1, desired_num_frames)
        interpolator = interpolate.interp1d(x_old, output_feature, kind='linear', fill_value='extrapolate')
        output_feature = interpolator(x_new)

    if normalize:
        output_feature = (output_feature - np.min(output_feature)) / (np.max(output_feature) - np.min(output_feature))
    return output_feature


def extractSection(path):
    result = allin1.analyze(path, device=CONF["device"])
    sections = []
    for idx, section in enumerate(result.segments):
        sections.append({
            "id": idx,
            "time": [section.start, section.end],
            "label": section.label
        })
    return sections
