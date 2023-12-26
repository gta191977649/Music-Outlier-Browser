from enum import Enum
class eNote(Enum):
    A = 1
    D = 2
    G = 3
    C = 4
    F = 5
    Bb = 6
    Eb = 7
    Ab = 8
    Db = 9
    Fsharp = 10
    B = 11
    E = 12

    @staticmethod
    def get_note_by_name(name: str):
        if name == "F#":
            name = "Fsharp"
        elif name == "A#":
            name = "Bb"
        elif name == "C#":
            name = "Db"
        elif name == "G#":
            name = "Ab"
        elif name == "D#":
            name = "Eb"
        elif name == "E#":
            name = "F"
        elif name == "B#":
            name = "C"
        elif name == "Gb":
            name = "Fsharp"
        a = eNote[name]
        return a
class Note:
    def __init__(self, note: eNote):
        self.note = note
        if not 1 <= self.note.value <= 12:
            raise ValueError("note index must be between 1 and 12")
        self.index = self.note.value

    @property
    def angle(self):
        return self.index * 30 - 15

    @property
    def name(self):
        return self.note.name

    @staticmethod
    def init_by_note_name(name: str):
        return eNote(eNote.get_note_by_name(name))

    def __repr__(self):
        return "{}".format(self.name.replace(
            "sharp","#"
        ))

    def angle_to(self, other):
        return (self - other) * 30

    # 获取从self到other逆时针方向的纯五跨度数
    def __sub__(self, other) -> int:
        if not isinstance(other, Note):
            raise TypeError(
                "unsupported operand type(s) for -: '_Note' and '{}'".format(type(other).__name__))
        if other.index == self.index:
            return 0
        interval = other.index - self.index
        return interval if interval > 0 else interval + 12

    def __gt__(self, other):
        return self.index > other.index

    def __lt__(self, other):
        return self.index < other.index
    def __eq__(self, other):
        return self.index == other.index

    def next(self, n=1):
        new_ind = self.index + n
        if n >= 0:
            if new_ind > 12:
                new_ind -= 12
        else:
            if new_ind <= 0:
                new_ind += 12

        return Note(eNote(new_ind))