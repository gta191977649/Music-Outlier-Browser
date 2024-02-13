def format_chord_progression(chords, time_signature=4):
    formatted_progression = []
    current_bar = []
    previous_chord = None

    for i, chord in enumerate(chords):
        if len(current_bar) == time_signature:
            # Join the chords in the current bar with commas and add to the formatted progression
            formatted_progression.append('| ' + ' '.join(current_bar) + ' |')
            current_bar = []
            previous_chord = None  # Reset previous_chord at the start of a new bar

        if chord == previous_chord:
            current_bar.append('.')
        else:
            current_bar.append(chord)
            previous_chord = chord

    # Add the last bar if it's not empty
    if current_bar:
        # Fill the remaining slots in the last bar with 'x' if it's not complete
        current_bar.extend(['.'] * (time_signature - len(current_bar)))
        formatted_progression.append('| ' + ' '.join(current_bar) + ' |')

    return ' '.join(formatted_progression)