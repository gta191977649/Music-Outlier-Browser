import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

y, sr = librosa.load('1091_WSI_SAD_XX_noise.wav')
S = librosa.feature.melspectrogram(y=y, sr=sr, power=1)
pcen_S = librosa.pcen(S,sr=sr)
log_S = librosa.amplitude_to_db(S, ref=np.max)



fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True)
img = librosa.display.specshow(log_S, x_axis='time', y_axis='mel', ax=ax[0])
ax[0].set(title='Mel Spectrogram', xlabel=None)
ax[0].label_outer()
imgpcen = librosa.display.specshow(pcen_S, x_axis='time', y_axis='mel', ax=ax[1])
ax[1].set(title='PCEN')
fig.colorbar(img, ax=ax[0], format="%+2.0f dB")
fig.colorbar(imgpcen, ax=ax[1])
plt.show()