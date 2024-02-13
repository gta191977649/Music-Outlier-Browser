import madmom, scipy.stats, numpy as np
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.downbeats import RNNDownBeatProcessor,DBNDownBeatTrackingProcessor

def extract_feature(file_path,feature):
    if feature == 'tempo':
        beats = madmom.features.beats.RNNBeatProcessor()(file_path)
        when_beats = madmom.features.beats.BeatTrackingProcessor(fps=100)(beats)
        m_res = scipy.stats.linregress(np.arange(len(when_beats)), when_beats)
        # first_beat = m_res.intercept
        beat_step = m_res.slope
        return 60/beat_step
    if feature == "deep_chroma":
        dcp = DeepChromaProcessor()
        chroma = dcp(file_path)
        return chroma
    if feature == "downbeats":
        beat_processor = RNNDownBeatProcessor()
        beat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)
        beats = beat_decoder(beat_processor(file_path))