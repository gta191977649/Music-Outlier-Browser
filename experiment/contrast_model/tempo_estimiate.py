import madmom, scipy.stats, numpy as np
beats = madmom.features.beats.RNNBeatProcessor()("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/similar_song/wav/蒲公英的约定.mp3")
when_beats = madmom.features.beats.BeatTrackingProcessor(fps=100)(beats)
m_res = scipy.stats.linregress(np.arange(len(when_beats)),when_beats)

first_beat = m_res.intercept 
beat_step = m_res.slope

print("bpm = ", 60/beat_step)