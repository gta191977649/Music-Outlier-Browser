import librosa
import h5.hdf5_getters as h5
import soundfile as sf
file = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult/h5/TRPSSSL128F4267C28.h5"
audio_preview = './beat_track.mp3'

# loading the fucking song
y, sr = librosa.load(audio_preview)

song = h5.open_h5_file_read(file)
beattimes = h5.get_beats_start(song)
bar_time = h5.get_bars_start(song)
section = h5.get_sections_start(song)


beat_frames = librosa.time_to_frames(beattimes,sr=sr)


clicks = librosa.clicks(frames=beat_frames, sr=sr, length=len(y))

y_click = y + clicks

sf.write('./beat_tracking_test.wav', y_click, sr)

