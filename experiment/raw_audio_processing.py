# This file deal with raw audio feature generation
# It will extracts the features and generate the song contrast using DTW modeling.
import librosa
import feature_extract as featureExtractor
import plot as plot
def loadFile(path):
    y,sr = librosa.load(path)
    print("File:{}\nSample Rate:{}".format(path,sr))
    return y, sr

def runPipeline(path):
    y,sr = loadFile(path)
    feature = featureExtractor.extractFeature(y,sr,type="loudness")
    print(feature)


if __name__ == '__main__':
    #runPipeline("../music/nogizaka_demo.wav")
    y,sr = loadFile("../music/サヨナラの意味.wav")
    loudness_mel = featureExtractor.extractFeature(y,sr,type="loudness",filterBank="mel")
    loudness_gamma = featureExtractor.extractFeature(y,sr,type="loudness",filterBank="gamma")
    plot.plot_signals([loudness_mel, loudness_gamma], labels=["Mel Filter Bank", "Gammatone Filter Bank"],title="Saiyounaranoimi - Nogizaka 48")