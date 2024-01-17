import matplotlib.pyplot as plt
import music21
import musicpy as mp
from Chord import *
import pandas as pd
import os
from matplotlib.pylab import mpl
plt.rcParams['font.sans-serif']=['Source Han Sans CN']
plt.rcParams['axes.unicode_minus']=False

def map_music21(chord_21):
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

# read midi file
FILENAME = r'../music/marigold_chord.mid'
midi = music21.converter.parse(FILENAME)
key = midi.analyze("key")
print(key)
chords = midi.chordify().flat.getElementsByClass(music21.chord.Chord)
chord_name_ls = []
chord_tension_ls = []
color_chord_ls = []
chord_theta_ls = []

current_note = None
for chord in chords:
    #chord_name_ls.append(chord.pitchedCommonName)
    # Elimiate next dulplicated note
    notes = map_music21(chord).getNotesArray()
    if not current_note == notes:
        chord_name_ls.append(mp.alg.detect(notes))
        chord_theta_ls.append(map_music21(chord).get_theta()[0])
        color_chord_ls.append(map_music21(chord))
        chord_tension_ls.append(map_music21(chord).get_harmony())
        current_note = notes


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
    'chord_tension': chord_tension_ls,
    'chord_theta_ls': chord_theta_ls,
    'color_change': color_change_ls,
    'tension_change': tension_change_ls,
    'freshness': freshness_ls})

df.to_csv("./contrast.csv")
x_values = range(len(df))

plt.figure(figsize=(12, 3))

# Tension
plt.subplot(1, 1, 1)
plt.plot(x_values, df['chord_theta_ls'], marker='o', color='b',drawstyle='steps-post',markersize=2)
plt.title('chord_theta_ls')
plt.ylabel('chord_theta_ls')
plt.xticks(x_values, df['chord_name'], rotation='vertical', fontsize=8)

plt.suptitle(os.path.basename(FILENAME), fontsize=16)
plt.tight_layout()
#plt.ylim(0, 100)
# Set x-axis limits
plt.xlim(left=0, right=max(x_values))

plt.show()
