from typing import List

from contrast_model.chromatic_chords import chromatic_chord as cc
import matplotlib.pyplot as plt
import numpy as np

## transform the chord in list format to colorChord format
## [C, E, G] -> [cNote.C, cNote.E, cNote.G]
def notes_to_cNotes(notes: List[Note]) -> List[cc.cNote]:
    return [cc.cNote.get_cNote_by_name(note) for note in notes]

## simplify the list of notes
## [C#b, E , F##] -> [C, E, G]
def simplify_chord(chord):
    output = []
    for note in chord:
        note = notes.reduce_accidentals(note)
        output.append(note)
    return output

## The list of chords to be used in the colorChord algorithm -- change as you wish
chord_list = ['C',"C#","D","D#","E","F","F#","G","G#","A","A#","B",
            'Cm',"C#m","Dm","D#m","Em","Fm","F#m","Gm","G#m","Am","A#m","Bm",
            'C7',"C#7","D7","D#7","E7","F7","F#7","G7","G#7","A7","A#7","B7",
            'Cm7',"C#m7","Dm7","D#m7","Em7","Fm7","F#m7","Gm7","G#m7","Am7","A#m7","Bm7",
            'Cmaj7',"C#maj7","Dmaj7","D#maj7","Emaj7","Fmaj7","F#maj7","Gmaj7","G#maj7","Amaj7","A#maj7","Bmaj7",
            'Cm7b5',"C#m7b5","Dm7b5","D#m7b5","Em7b5","Fm7b5","F#m7b5","Gm7b5","G#m7b5","Am7b5","A#m7b5","Bm7b5"]


c_notes_list = [cc.Chord(notes_to_cNotes(simplify_chord(chords.from_shorthand(chord))), name = chord) for chord in chord_list]
#print(c_notes_list)

data = [((chord.get_harmony(), min(chord.get_theta())),chord.name) for chord in c_notes_list]


# Convert data to arrays of distances, angles, and labels
distances, angles, labels = zip(*[(d, np.deg2rad(theta), label) for (d, theta), label in data])

# Create polar plot
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.set_theta_zero_location('E')

# Plot points with labels
# Plot points with labels
for distance, angle, label in zip(distances, angles, labels):
    ax.plot(angle, distance, 'o', label=label)
    ax.text(angle, distance, label, ha='left', va='bottom', fontsize= 'x-small', fontfamily= "cursive")
# Add gridlines and legend

ax.grid(True)

## hide the labels (not necessary)
ax.tick_params(axis='both', labelcolor='none')



# Show plot
plt.show()

