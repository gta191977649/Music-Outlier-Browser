import numpy as np
from scipy.io import wavfile
import audiotsm
import audiotsm.io.wav

# Load the audio file
fs, audio = wavfile.read("1091_WSI_SAD_XX_noise.wav")

# Define the reverb parameters
room_size = 50  # in meters
reverb_time = 1  # in seconds
damping = 0.5  # controls the decay time of the reverb effect

# Compute the reverb filter coefficients
alpha = np.exp(-2*np.pi*reverb_time/room_size)
b = [1 - alpha]
a = [1, -damping*alpha]

# Apply the reverb filter to the audio signal
reverb_audio = audiotsm.base.input_output_filter(audio, b, a)

# Save the reverb audio to a new WAV file
audiotsm.io.wav.write("output.wav", reverb_audio, fs)
