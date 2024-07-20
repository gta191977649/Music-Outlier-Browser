import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# Load audio file
audio_file = '../music/nogizaka_demo.wav'
y, sr = librosa.load(audio_file,duration=30)

# Beat tracking
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print(f"Tempo: {tempo}")
print(f"Beat frames: {beat_frames}")

# Convert beat frames to samples
beat_samples = librosa.frames_to_samples(beat_frames)

# Generate click track
clicks = librosa.clicks(frames=beat_frames, sr=sr, length=len(y))

# Add click track to original audio
y_click = y + clicks

# Save the audio with clicks
sf.write('music/konayuki.mp3', y_click, sr)

# Segment the audio signal into beats
segments = [y[start:end] for start, end in zip(beat_samples[:-1], beat_samples[1:])]

# Take the absolute value of each segment
abs_segments = [np.abs(segment) for segment in segments]

# Compute the self-similarity matrix
num_segments = len(abs_segments)
ssm = np.zeros((num_segments, num_segments))

for i in range(num_segments):
    for j in range(num_segments):
        # Zero-pad the shorter segment
        len_i = len(abs_segments[i])
        len_j = len(abs_segments[j])
        if len_i < len_j:
            pad_len = len_j - len_i
            segment_i = np.pad(abs_segments[i], (0, pad_len))
            segment_j = abs_segments[j]
        else:
            pad_len = len_i - len_j
            segment_i = abs_segments[i]
            segment_j = np.pad(abs_segments[j], (0, pad_len))

        ssm[i, j] = np.sum(segment_i * segment_j)

# Plot the self-similarity matrix
plt.figure(figsize=(10, 8))
plt.imshow(ssm, cmap='hot', interpolation='nearest')
plt.title('Self-Similarity Matrix')
plt.xlabel('Beat Index')
plt.ylabel('Beat Index')
plt.colorbar(label='Similarity')
plt.show()
