import madmom, scipy.stats, numpy as np
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.downbeats import RNNDownBeatProcessor,DBNDownBeatTrackingProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
from madmom.features.chords import DeepChromaChordRecognitionProcessor,CRFChordRecognitionProcessor,CNNChordFeatureProcessor
from pychord import Chord

def extract_chord(file):
    # detect chord
    dcp = DeepChromaProcessor()
    decode = DeepChromaChordRecognitionProcessor()
    chroma = dcp(file)
    chords = decode(chroma)
    # detect beats
    beat_processor = RNNDownBeatProcessor()
    beat_decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)
    beats = beat_decoder(beat_processor(file))
    return chords,beats

def transpose_chord(chord_str, transpose_amount,target_scale):
    chord = Chord(chord_str)
    chord.transpose(transpose_amount,scale=target_scale)
    #chord.transpose(transpose_amount)
    transposed_chord = chord
    return transposed_chord
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
    if feature == "key":
        proc = CNNKeyRecognitionProcessor()(file_path)
        return key_prediction_to_label(proc),proc

    # if feature == "time_sig":


def chord_to_roman(chords, is_major=True):
    # Mapping for C major
    major_map = {
        'Cmaj': 'I', 'Dmin': 'ii', 'Emin': 'iii', 'Fmaj': 'IV',
        'Gmaj': 'V', 'Amin': 'vi', 'Bdim': 'vii°'
    }

    # Mapping for A minor
    minor_map = {
        'Amin': 'i', 'Bdim': 'ii°', 'Cmaj': 'III', 'Dmin': 'iv',
        'Emin': 'v', 'Fmaj': 'VI', 'Gmaj': 'VII'
    }

    roman_numerals = []

    # Choose the appropriate mapping based on the key
    chord_map = major_map if is_major else minor_map

    # Convert each chord to its Roman numeral equivalent
    for chord in chords:
        roman_numerals.append(chord_map.get(chord, "?"))  # Use "?" for unmatched chords

    return tuple(roman_numerals)