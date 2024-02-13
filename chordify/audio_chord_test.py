# import autochord
import io

import h5.hdf5_getters as h5
import numpy as np
import librosa
import matplotlib.pyplot as plt
from pathlib import Path

#
#
#
# path = "../data/blue_oyster_cult/TRXPLQW128F92C2C21.h5"
# file = h5.open_h5_file_read(path)
# chroma_2 = h5.get_segments_pitches(file)
# title = h5.get_title(file)
# chroma = autochord.generate_chroma("../music/bic.mp3")
# librosa.display.specshow(chroma.T, y_axis='chroma', x_axis='time')
# plt.title('Chromagram')
# plt.tight_layout()
# plt.show()


import madmom
import numpy as np
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor,CRFChordRecognitionProcessor,CNNChordFeatureProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label


PATH = '../music/bic_camera_2.mp3'


dcp = DeepChromaProcessor()
decode = DeepChromaChordRecognitionProcessor()
chroma = dcp(PATH)

chords = decode(chroma)
#
# featproc = CNNChordFeatureProcessor()
# feats = featproc(PATH)
# decode_cnn = CRFChordRecognitionProcessor()
# chords = decode_cnn(feats)

lab_file = ""
for chord in chords:

    start,end,name =chord
    print(start,end,name)
    lab_file += "{}\t{}\t{}\n".format(start,end,name)

f = open(PATH+".lab","w")
f.write(lab_file)
f.close()

# librosa.display.specshow(chroma.T, y_axis='chroma', x_axis='time')
# plt.show()