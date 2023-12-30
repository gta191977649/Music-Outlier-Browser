from chord_extractor.extractors import Chordino
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Chordino
chordino = Chordino(roll_on=1)

# Run extraction on the provided MIDI file
chords = chordino.extract('E:\\dev\\Music-Outlier-Browser\\music\\special\\4536251\\zcddy_chord.mid')

# Create a list to store chord names, initializing with 0
chord_name_ls = [0]

# Extract chord names from the extracted chords and add them to the list
for c in chords:
    chord_name_ls.append(c.chord)

# Create a DataFrame from the chord names
df = pd.DataFrame({
    'chord_name': chord_name_ls
})

# Counting the frequency of each chord
chord_counts = df['chord_name'].value_counts()

# Plotting the bar chart
plt.figure(figsize=(10, 6))
chord_counts.plot(kind='bar')
plt.xlabel('Chord Name')
plt.ylabel('Frequency')
plt.title('Frequency of Chords')
plt.xticks(rotation=45)
plt.show()
