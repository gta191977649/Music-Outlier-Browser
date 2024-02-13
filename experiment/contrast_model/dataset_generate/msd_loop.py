import os
import h5.hdf5_getters as h5
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor,CRFChordRecognitionProcessor,CNNChordFeatureProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
from madmom.features.downbeats import RNNDownBeatProcessor,DBNDownBeatTrackingProcessor

if __name__ == '__main__':
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/blue_oyster_cult"
    TRANSPOSED = True
    PATH_H5_DIR = os.path.join(BASE_PATH, "h5")
    for root, dirs, files in os.walk(PATH_H5_DIR):
        for idx, filename in enumerate(files):
            if os.path.splitext(filename)[1] == ".h5":
                CHORD_FILENAME = filename.replace(".h5", "_transposed.lab" if TRANSPOSED else ".lab")
                FILE_NAME_WAV = filename.replace(".h5", ".wav")
                PATH_WAV = os.path.join(BASE_PATH,"wav" ,FILE_NAME_WAV)
                PATH_H5_FILE = os.path.join(root, filename)
                file = h5.open_h5_file_read(PATH_H5_FILE)
                time_signature = h5.get_time_signature(file)
                if os.path.exists(PATH_WAV):
                    title = h5.get_title(file).decode('utf-8')
                    print(time_signature,title)

