def calculate_chords(circle_of_fifths, min_fifth_span, max_fifth_span, min_notes, max_notes):
    # 将五度圈音符映射到它们的索引
    note_indices = {note: index for index, note in enumerate(circle_of_fifths)}

    # 检查和弦是否符合五度圈跨度限制
    def is_valid_chord(chord):
        indices = [note_indices[note] for note in chord]
        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                span = min(abs(indices[j] - indices[i]), len(circle_of_fifths) - abs(indices[j] - indices[i]))
                if span < min_fifth_span or span > max_fifth_span:
                    return False
        return True

    # 递归地构建和弦
    def build_chords(chord, remaining_notes):
        if len(chord) == remaining_notes:
            if is_valid_chord(chord):
                valid_chords.add(tuple(sorted(chord)))  # 加入已排序的和弦以避免重复
            return
        for note in circle_of_fifths:
            build_chords(chord + [note], remaining_notes)

    valid_chords = set()
    for num_notes in range(min_notes, max_notes + 1):
        build_chords([], num_notes)

    return valid_chords

# 五度圈
circle_of_fifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']

# 计算3至6个音的和弦结构
chords = calculate_chords(circle_of_fifths, 2, 10, 3, 6)
print("Total number of chords:", len(chords))
