from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor,CRFChordRecognitionProcessor,CNNChordFeatureProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
from madmom.features.downbeats import RNNDownBeatProcessor,DBNDownBeatTrackingProcessor
import librosa
import soundfile as sf

if __name__ == '__main__':
    audio_file_name = "../music/final_countdown.mp3"
    chord_processor = DeepChromaProcessor()
    chord_decoder = DeepChromaChordRecognitionProcessor()
    chords = chord_decoder(chord_processor(audio_file_name))

    # detect beats
    beat_processor = RNNDownBeatProcessor()
    beat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)
    beats = beat_decoder(beat_processor(audio_file_name))

    # generate chord with beats aligned
    chordsArray = []
    chord_idx = 0
    for beat_idx in range(len(beats) - 1):
        curr_beat_time, curr_beat = beats[beat_idx]
        # find the corresponding chord for this beat
        while chord_idx < len(chords):
            chord_time, _, _ = chords[chord_idx]
            prev_beat_time, _ = (0, 0) if beat_idx == 0 else beats[beat_idx - 1]
            eps = (curr_beat_time - prev_beat_time) / 2
            if chord_time > curr_beat_time + eps:
                break
            chord_idx += 1

        # append to array
        _, _, prev_chord = chords[chord_idx - 1]
        chord = (curr_beat_time, curr_beat, prev_chord)

        chordsArray.append(chord)

    # Generate chord label file
    lab_file = ""
    for c in chordsArray:
        curr_beat_time, curr_beat, prev_chord = c
        print(curr_beat_time, curr_beat, prev_chord)
        lab_file += "{}\t{}\t{}\n".format(curr_beat_time, curr_beat, prev_chord)

    bts = []
    for b in beats:
        bts.append(b[0])

    f = open(audio_file_name + ".lab", "w")
    f.write(lab_file)
    f.close()

    y, sr = librosa.load(audio_file_name)
    beat_frames = librosa.time_to_frames(bts, sr=sr)
    clicks = librosa.clicks(frames=beat_frames, sr=sr, length=len(y))
    y_click = y + clicks
    sf.write('./beat_tracking_test.wav', y_click, sr)

