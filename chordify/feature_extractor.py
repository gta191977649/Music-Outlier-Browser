import madmom, scipy.stats, numpy as np
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.downbeats import RNNDownBeatProcessor,DBNDownBeatTrackingProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label
from madmom.features.chords import DeepChromaChordRecognitionProcessor,CRFChordRecognitionProcessor,CNNChordFeatureProcessor
from pychord import Chord
from contrast_model.Chord import eNote
from contrast_model.Chord import Chord as VectorModel

def map_music21(chord_21,name):
    map_21 = {'A': eNote.A,
              'D': eNote.D,
              'G': eNote.G,
              'C': eNote.C,
              'F': eNote.F,
              'Bb': eNote.Bb,
              'A#': eNote.Bb,
              'Eb': eNote.Eb,
              'D#': eNote.Eb,
              'G#': eNote.Ab,
              'Ab': eNote.Ab,
              'C#': eNote.Db,
              'Db': eNote.Db,
              'F#': eNote.Fsharp,
              'Gb': eNote.Fsharp,
              'B': eNote.B,
              'E': eNote.E}
    temp = []
    for i in chord_21:
        temp.append(map_21[i])

    return VectorModel(temp,name=name)
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
def getChordVectorsFromFile(PATH_CHORD):
    chords = []
    with open(PATH_CHORD, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Skip the line if it starts with '#'
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) == 3:
                start, end, chord_str = parts
                # SKIP NONE CHORD
                if chord_str in ["N", "None"]: continue
                chord_str = chord_str.replace(":","")
                c = Chord(chord_str)
                notes = c.components()
                v = map_music21(notes, chord_str)
                chords.append({
                    "chord":v,
                    "name":chord_str,
                    "angle":v.temp_theta,
                    "beat":end,
                })
    return chords
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

    chromatic_chord_map_major = {
        'Cmaj': 'I',  # Diatonic in C major
        'C#dim': 'bii°',  # Not diatonic in C major (would be diatonic in C# harmonic/melodic minor)
        'Dmin': 'ii',  # Diatonic in C major
        'D#dim': 'biii°',  # Not diatonic in C major (would be diatonic in Eb harmonic/melodic minor)
        'Emaj': 'III',  # Not diatonic in C major (E is minor in C major)
        'Fmin': 'iv',  # Not diatonic in C major (F is major in C major)
        'Fmaj': 'IV',  # Diatonic in C major
        'F#dim': '#iv°',  # Not diatonic in C major (would be diatonic in F# harmonic/melodic minor)
        'Gmaj': 'V',  # Diatonic in C major
        'G#dim': 'bvi°',  # Not diatonic in C major (would be diatonic in Ab harmonic/melodic minor)
        'Amin': 'vi',  # Diatonic in C major
        'BbMaj': 'bVII',  # Not diatonic in C major (Bb is not in C major scale)
        'Bdim': 'vii°',  # Diatonic in C major
    }

    chromatic_chord_map_minor = {
        'Cmin': 'i',  # Diatonic in C natural minor
        'C#min': 'ii°',  # Not diatonic in C natural minor (would be diatonic in C harmonic/melodic minor)
        'Dmin': 'ii',  # Not diatonic in C natural minor (D is diminished in C natural minor)
        'D#maj': 'III',  # Diatonic in C natural minor
        'Emaj': 'III+',  # Not diatonic in C natural minor (E is diminished in C natural minor)
        'Emin': 'iii',  # Not diatonic in C natural minor (E is diminished in C natural minor)
        'Fmin': 'iv',  # Diatonic in C natural minor
        'Fmaj': 'IV',  # Not diatonic in C natural minor (F is minor in C natural minor)
        'F#min': '#iv°',  # Not diatonic in C natural minor (F# is not in C natural minor scale)
        'Gmin': 'v',  # Diatonic in C natural minor
        'Gmaj': 'V',  # Not diatonic in C natural minor (G is minor in C natural minor)
        'G#maj': 'VI',  # Diatonic in C natural minor
        'Abmaj': 'VI',  # Not diatonic in C natural minor (G# is raised in C harmonic/melodic minor)
        'Amin': 'vii',  # Not diatonic in C natural minor (A is major in C harmonic minor)
        'Amaj': 'VII',  # Not diatonic in C natural minor (A is major in C harmonic minor)
        'Bbmin': 'vii°',  # Not diatonic in C natural minor (Bb is major in C natural minor)
        'Bbmaj': 'bVII',  # Diatonic in C natural minor
        'Bmin': 'vii°',  # Diatonic in C harmonic minor (B natural would be part of the harmonic minor scale)
        'Bmaj': 'VII+',  # Not diatonic in C natural minor (B is diminished in C natural minor)
    }

    # Mapping for A minor
    minor_map = {
        'Amin': 'i', 'Bdim': 'ii°', 'Cmaj': 'III', 'Dmin': 'iv',
        'Emin': 'v', 'Fmaj': 'VI', 'Gmaj': 'VII'
    }

    roman_numerals = []

    # Choose the appropriate mapping based on the key
    #chord_map = major_map if is_major else minor_map
    chord_map = chromatic_chord_map_major if is_major else chromatic_chord_map_minor

    # Convert each chord to its Roman numeral equivalent
    for chord in chords:
        roman_numerals.append(chord_map.get(chord, "?"))  # Use "?" for unmatched chords

    return tuple(roman_numerals)