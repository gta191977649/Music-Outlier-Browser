import librosa
y, sr = librosa.load('../music/title.mp3')
pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
# Extracting the main pitch from each frame
main_pitches = [pitch[magnitudes[:, idx].argmax()] for idx, pitch in enumerate(pitches.T) if magnitudes[:, idx].max() > 0]
range_value = max(main_pitches) - min(main_pitches)
print(f"Range: {range_value} Hz")
