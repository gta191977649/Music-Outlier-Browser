from itertools import combinations

notes_semitones = {
    'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11, 'F#': 6,
    'Db': 1, 'Ab': 8, 'Eb': 3, 'Bb': 10, 'F': 5
}

notes_order = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

intervals_within_sixth = list(range(10))

def note_from_root(root, semitones):
    root_position = notes_semitones[root]
    note_position = (root_position + semitones) % 12
    for note, position in notes_semitones.items():
        if position == note_position:
            return note
    return None

def generate_chords_within_sixth(root, notes_semitones):
    chords = []
    for combo in combinations(intervals_within_sixth, 3):  # Three-note chords
        chord_notes = [root] + [note_from_root(root, semitones) for semitones in combo[1:]]
        chords.append(chord_notes)
    return chords

all_chords_within_sixth = {}
for root_note in notes_order:
    all_chords_within_sixth[root_note] = generate_chords_within_sixth(root_note, notes_semitones)

for root_note, chords in all_chords_within_sixth.items():
    print(f"Chords within a sixth for {root_note}:")
    for chord in chords:
        print(chord)
    print("\n")
