# Parncutt's model
import numpy as np

def frequency(note):
    # A4 is set as the reference note, with a frequency of 440 Hz.
    # The note is given as the number of semitones from A4.
    A4_freq = 440
    return A4_freq * (2 ** (note / 12))

def roughness(freq1, freq2):
    # Constants for the roughness calculation (These are just example values;
    # you would need to determine appropriate values through experimentation or literature review)
    a = 3.5
    b = 5.75
    model_roughness = np.exp(-b * abs(freq2 - freq1)) * (1 - np.exp(-a * abs(freq2 - freq1)))
    return model_roughness

notes_C_major = {'C': -9, 'E': -5, 'G': -2}

frequencies = {note: frequency(semi) for note, semi in notes_C_major.items()}

total_roughness = 0
for note1 in notes_C_major:
    for note2 in notes_C_major:
        if note1 < note2:  # Avoid calculating the same pair twice
            total_roughness += roughness(frequencies[note1], frequencies[note2])

print(f"The roughness of the C major chord is: {total_roughness}")
