import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import soundfile as sf
# Load audio file
audio_file = '../music/nogizaka_demo.wav'
y, sr = librosa.load(audio_file)

# Beat tracking
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_samples = librosa.frames_to_samples(beat_frames)

# Segment the audio signal into beats
segments = [y[start:end] for start, end in zip(beat_samples[:-1], beat_samples[1:])]

# Take the absolute value of each segment
abs_segments = [np.abs(segment) for segment in segments]

# Compute chroma features for each segment
chroma_segments = [librosa.feature.chroma_stft(y=segment, sr=sr) for segment in segments]

# Compute the self-similarity matrix for ABS
ssm_abs = np.zeros((len(abs_segments), len(abs_segments)))
for i in range(len(abs_segments)):
    for j in range(len(abs_segments)):
        if len(abs_segments[i]) < len(abs_segments[j]):
            pad_len = len(abs_segments[j]) - len(abs_segments[i])
            abs_i = np.pad(abs_segments[i], (0, pad_len))
            abs_j = abs_segments[j]
        else:
            pad_len = len(abs_segments[i]) - len(abs_segments[j])
            abs_i = abs_segments[i]
            abs_j = np.pad(abs_segments[j], (0, pad_len))
        ssm_abs[i, j] = np.sum(abs_i * abs_j)

# Compute the self-similarity matrix for Chroma
ssm_chroma = np.zeros((len(chroma_segments), len(chroma_segments)))
for i in range(len(chroma_segments)):
    for j in range(len(chroma_segments)):
        # Zero-pad the shorter chroma segment
        if chroma_segments[i].shape[1] < chroma_segments[j].shape[1]:
            pad_len = chroma_segments[j].shape[1] - chroma_segments[i].shape[1]
            chroma_i = np.pad(chroma_segments[i], ((0, 0), (0, pad_len)), 'constant')
            chroma_j = chroma_segments[j]
        else:
            pad_len = chroma_segments[i].shape[1] - chroma_segments[j].shape[1]
            chroma_i = chroma_segments[i]
            chroma_j = np.pad(chroma_segments[j], ((0, 0), (0, pad_len)), 'constant')

        ssm_chroma[i, j] = np.sum(chroma_i * chroma_j)

# Convert chroma_segments to a 2D NumPy array for plotting
beat_chroma = np.array([np.mean(segment, axis=1) for segment in chroma_segments]).T

# Compute the original chroma features for the entire audio signal
#original_chroma = librosa.feature.chroma_stft(y=y, sr=sr)
original_chroma = librosa.feature.chroma_cens(y=y, sr=sr)

# Plotting
plt.figure(figsize=(10, 10))
gs = gridspec.GridSpec(3, 2, width_ratios=[1, 1], height_ratios=[1, 0.4, 0.4],hspace=0.25)

# ABS beats SSM
ax0 = plt.subplot(gs[0, 0])
plt.imshow(ssm_abs, cmap='hot', interpolation='nearest')
plt.title('Beat Segement ABS SSM')

# Chroma beats SSM
ax1 = plt.subplot(gs[0, 1])
plt.imshow(ssm_chroma, cmap='hot', interpolation='nearest')
plt.title('Beat Segement Chroma SSM')

# Beat-synchronous Chromagram
ax2 = plt.subplot(gs[1, :])
librosa.display.specshow(beat_chroma, x_axis='frames', y_axis='chroma')
plt.title('Beat Segement Chroma')

# Original Chromagram
ax3 = plt.subplot(gs[2, :])
librosa.display.specshow(original_chroma, x_axis='time', y_axis='chroma')
plt.title('Original Chroma')

# Remove padding
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.15)

# Generate beat tracking debug file
clicks = librosa.clicks(frames=beat_frames, sr=sr, length=len(y))

# Add click track to original audio
y_click = y + clicks

# Save the audio with clicks
sf.write('beat_tracking_test.wav', y_click, sr)


plt.show()
