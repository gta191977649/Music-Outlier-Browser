from contrast_model.Chord import Chord as VectorModel
from contrast_model.Chord import eNote
from pychord import Chord
import pandas as pd

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
                start, beat, chord_str = parts
                # SKIP NONE CHORD
                if chord_str in ["N", "None"]:
                    chords.append({
                        "angle": 0,
                        "start": start,
                        "beat": beat,
                    })
                    continue

                chord_str = chord_str.replace(":", "")

                c = Chord(chord_str)
                notes = c.components()
                v = map_music21(notes, chord_str)
                chords.append({
                    "angle":v.temp_theta,
                    "start":start,
                    "beat":beat,
                })
    return chords

if __name__ == '__main__':
    PATH_CHORD = "/music/final_countdown.mp3.lab"

    chords = getChordVectorsFromFile(PATH_CHORD)

    chord_name_ls = []
    chord_theta_ls = []
    chord_start_ls = []
    chord_beat_ls = []

    VEC_FILE_BUFFER = ""
    # Loop through Chords
    for c in chords:
        VEC_FILE_BUFFER += "{} {} {}\n".format(float(c["start"]),float(c["beat"]),c["angle"])

    print(VEC_FILE_BUFFER)


    audio_file_name = PATH_CHORD.replace(".lab",".vec")
    f = open(audio_file_name, "w")
    f.write(VEC_FILE_BUFFER)
    f.close()

