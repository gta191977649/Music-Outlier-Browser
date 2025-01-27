import matplotlib.pyplot as plt
import music21
from contrast_model.chromatic_chords.chromatic_chord import *
import pandas as pd

def map_music21(chord_21):
    map_21 = {'A': cNote.A,
              'D': cNote.D,
              'G': cNote.G,
              'C': cNote.C,
              'F': cNote.F,
              'B-': cNote.Bb,
              'E-': cNote.Eb,
              'G#': cNote.Ab,
              'C#': cNote.Db,
              'F#': cNote.Fsharp,
              'B': cNote.B,
              'E': cNote.E}
    temp = []
    for i in chord_21.notes:
        temp.append(map_21[i.name])

    return Chord(temp)

# read midi file
midi = music21.converter.parse(r'../music/marigorudo_music_box_30sec.mid')
chords = midi.chordify().flat.getElementsByClass(music21.chord.Chord)

chord_name_ls = []
color_chord_ls = []
for chord in chords:
    chord_name_ls.append(chord.pitchedCommonName)
    color_chord_ls.append(map_music21(chord))

color_change_ls = [0]
tension_change_ls = [0]
freshness_ls = [0]

for i in range(len(chord_name_ls) - 1):
    a = color_chord_ls[i]
    b = color_chord_ls[i+1]
    color_change_ls.append(Chord.get_color_change(a, b))
    tension_change_ls.append(Chord.get_tension_change(a, b))
    freshness_ls.append(Chord.get_fressness(a, b))


df = pd.DataFrame({
    'chord_name': chord_name_ls,
    'color_change': color_change_ls,
    'tension_change': tension_change_ls,
    'freshness': freshness_ls})

x_values = range(len(df))

plt.figure(figsize=(12,8))

plt.subplot(3, 1, 1)
plt.plot(x_values, df['color_change'], marker='o', color='b')
plt.title('Color Change')
plt.ylabel('Color Change')

# Tension Change
plt.subplot(3, 1, 2)
plt.plot(x_values, df['tension_change'], marker='o', color='r')
plt.title('Tension Change')
plt.ylabel('Tension Change')

# Freshness
plt.subplot(3, 1, 3)
plt.plot(x_values, df['freshness'], marker='o', color='g')
plt.title('Freshness')
plt.ylabel('Freshness')
plt.xlabel('Chord Name')

plt.tight_layout()
plt.show()