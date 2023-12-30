import musicpy as mp
import music21

midi = music21.converter.parse("E:\\dev\\Music-Outlier-Browser\\music\\special\\4536251\\zcddy_chord.mid")
chords = midi.chordify().flat.getElementsByClass(music21.chord.Chord)
for chord in chords:
    notes = []
    for note in chord.notes:
        key = note.name
        key = key.replace("+","#")
        key = key.replace("-","b")
        notes.append(key)
    keys = ','.join(notes)
    chord_name = mp.alg.detect(keys)
    print(chord_name)

