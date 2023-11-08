import librosa
import numpy as np
import matplotlib.pyplot as plt

y, sr = librosa.load('../music/aozoragahigauutawari.mp3')

# Onset detection
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

# Calculate beat intervals
beat_intervals = np.diff(beats)

# Histogram of beat intervals
hist, bin_edges = np.histogram(beat_intervals, bins=np.arange(0, max(beat_intervals) + 2) - 0.5)

# Time signature estimation based on histogram peaks
most_common_interval = bin_edges[np.argmax(hist)]
if 0.66 < most_common_interval < 1.5:
    time_signature = "2/4"
elif 1.5 < most_common_interval < 2.5:
    time_signature = "3/4"
elif 2.5 < most_common_interval < 3.5:
    time_signature = "4/4"
else:
    time_signature = "Unknown"

print(f"Estimated time signature: {time_signature}")

# Visualization of onset curve, beats, and histogram
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(librosa.times_like(onset_env, sr=sr), onset_env, label='Onset strength')
plt.vlines(librosa.frames_to_time(beats, sr=sr), 0, onset_env.max(), color='r', alpha=0.9, linestyle='--', label='Beats')
plt.xlabel('Time (s)')
plt.legend()

plt.subplot(1, 2, 2)
plt.bar(bin_edges[:-1], hist, width=1)
plt.xlabel('Beat intervals')
plt.ylabel('Count')
plt.tight_layout()

plt.show()
