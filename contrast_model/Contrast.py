import music21
from contrast_model.Chord import *
import pandas as pd

class Contrast:
    def __init__(self,file):
        self.file = file

    def map_music21(self,chord_21):
        map_21 = {'A': eNote.A,
                  'D': eNote.D,
                  'G': eNote.G,
                  'C': eNote.C,
                  'F': eNote.F,
                  'B-': eNote.Bb,
                  'E-': eNote.Eb,
                  'G#': eNote.Ab,
                  'C#': eNote.Db,
                  'F#': eNote.Fsharp,
                  'B': eNote.B,
                  'E': eNote.E}
        temp = []
        for i in chord_21.notes:
            temp.append(map_21[i.name])

        return Chord(temp)

    import music21
    import pandas as pd

    def anlysis(self):
        file = self.file
        midi = music21.converter.parse(file)
        chords = midi.chordify().flat.getElementsByClass(music21.chord.Chord)
        default_tempo = 120
        tempo = midi.metronomeMarkBoundaries()[0][2].number if midi.metronomeMarkBoundaries() else default_tempo
        print(tempo)
        chord_name_ls = []
        chord_tension_ls = []
        color_chord_ls = []
        chord_timing_ls = []

        for chord in chords:
            chord_name_ls.append(chord.pitchedCommonName)
            mapped_chord = self.map_music21(chord)
            color_chord_ls.append(mapped_chord)
            chord_tension_ls.append(mapped_chord.get_harmony())

            # Calculate start time, duration, and end time
            start_time_in_seconds = float(chord.offset * 60 / tempo)
            duration_in_seconds = float(chord.duration.quarterLength * 60 / tempo)
            end_time_in_seconds = float(start_time_in_seconds + duration_in_seconds)

            chord_timing_ls.append([start_time_in_seconds, duration_in_seconds, end_time_in_seconds])

        color_change_ls = [0]
        tension_change_ls = [0]
        freshness_ls = [0]

        for i in range(len(chord_name_ls) - 1):
            a = color_chord_ls[i]
            b = color_chord_ls[i + 1]
            color_change_ls.append(Chord.get_color_change(a, b))
            tension_change_ls.append(Chord.get_tension_change(a, b))
            freshness_ls.append(Chord.get_fressness(a, b))

        df = pd.DataFrame({
            'chord_name': chord_name_ls,
            'chord_tension': chord_tension_ls,
            'color_change': color_change_ls,
            'tension_change': tension_change_ls,
            'freshness_ls': freshness_ls,
            'chord_timing_ls':chord_timing_ls,
        })
        print(chord_timing_ls)
        return df
