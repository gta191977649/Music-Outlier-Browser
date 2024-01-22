
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import h5.hdf5_getters as h5
import scipy

# chord = autochord.recognize('../music/bic.mp3', lab_fn='../music/bic.lab')
path = "../data/blue_oyster_cult/TRASNUX128F425EAF2.h5"
file = h5.open_h5_file_read(path)
chroma = h5.get_segments_pitches(file)
time = h5.get_duration(file)
artist = h5.get_artist_name(file)
name  =h5.get_title(file)
key = h5.get_key(file)

plt.figure(figsize=(10, 4))

chroma_filter = np.minimum(chroma.T,librosa.decompose.nn_filter(chroma.T,aggregate=np.median,metric='cosine'))
chroma_smooth = scipy.ndimage.median_filter(chroma_filter, size=(1, 9))

librosa.display.specshow(chroma.T, y_axis='chroma', x_axis='time')

plt.title('Chromagram')
plt.tight_layout()
plt.show()