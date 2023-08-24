import librosa
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

# Load audio file
y, sr = librosa.load('../music/nogizaka_demo.wav',duration=20)  # Replace with your audio file

# Beat detection
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

# Convert beats to time
beat_times = librosa.frames_to_time(beats, sr=sr)

# Generate Mel spectrogram
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
S_dB = librosa.power_to_db(S, ref=np.max)

# Generate clicks at beat times
clicks = librosa.clicks(times=beat_times, sr=sr, length=len(y))

# Add clicks to original audio
y_clicks = y + clicks

# Save the audio with clicks
sf.write('original_clicks.wav', y_clicks, sr)

# Maximum time
max_time = len(y) / sr

# Create subplots
fig, axs = plt.subplots(2, 1, figsize=(15, 10))

# Plot original waveform
axs[0].plot(np.linspace(0, max_time, len(y)), y, label='Original Waveform')
axs[0].set_title(f'Original Waveform - Detected Tempo: {tempo} BPM')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_xlim([0, max_time])
for beat_time in beat_times:
    axs[0].axvline(x=beat_time, color='r', linestyle='--', linewidth=1, label='Beat')

# Plot Mel spectrogram
librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=axs[1])
axs[1].set_title(f'Mel Spectrogram - Detected Tempo: {tempo} BPM')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Mel Frequency')
axs[1].set_xlim([0, max_time])
for beat_time in beat_times:
    axs[1].axvline(x=beat_time, color='r', linestyle='--', linewidth=1, label='Beat')

# Show plots
plt.tight_layout()
plt.show()
