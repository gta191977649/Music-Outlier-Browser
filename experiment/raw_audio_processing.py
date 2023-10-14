# This file deal with raw audio feature generation
# It will extracts the features and generate the song contrast using DTW modeling.
import librosa
import feature_extract as featureExtractor
import plot as plot
def loadFile(path):
    y,sr = librosa.load(path)
    print("File:{}\nSample Rate:{}".format(path,sr))
    return y, sr

def embeddingSectonFeature(sr,sections, feature):
    hop_length = 512
    for section in sections:
        start_time, end_time = section["time"]
        # Convert time to frames
        start_frame = librosa.time_to_frames(start_time, sr=sr, hop_length=hop_length)
        end_frame = librosa.time_to_frames(end_time, sr=sr, hop_length=hop_length)
        # Extract the features for this section
        section["feature"] = feature[start_frame:end_frame]
    return sections



if __name__ == '__main__':
    # 1. load file
    path = "../music/aozoragahigauutawari.mp3"
    y, sr = loadFile(path)
    # 2. extract features
    loudness_mel = featureExtractor.extractFeature(y, sr, type="loudness",filterBank="mel")
    loudness_gamma = featureExtractor.extractFeature(y, sr, type="loudness",filterBank="gamma")
    section = featureExtractor.extractSection(path)
    section = embeddingSectonFeature(sr,section,loudness_gamma)

    plot.plot_signals([loudness_mel, loudness_gamma], labels=["Mel Filter Bank", "Gammatone Filter Bank"],
                      title="Saiyounaranoimi - Nogizaka 48")
    plot.plot_signals_by_sections(section,title=path)

    # Filter Bank Test
    # y, sr = loadFile("../music/サヨナラの意味.wav")
    # loudness_mel = featureExtractor.extractFeature(y,sr,type="loudness",filterBank="mel")
    # loudness_gamma = featureExtractor.extractFeature(y,sr,type="loudness",filterBank="gamma")
    # plot.plot_signals([loudness_mel, loudness_gamma], labels=["Mel Filter Bank", "Gammatone Filter Bank"],title="Saiyounaranoimi - Nogizaka 48")