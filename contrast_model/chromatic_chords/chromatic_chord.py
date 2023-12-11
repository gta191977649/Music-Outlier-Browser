import math
from enum import Enum
from itertools import combinations


class cNote(Enum):
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
    def get_cNote_by_name(name: str):
        '''
        通过字符串格式的音名获取cNote对象
        :param name: 音符名称str,如 name = "Bb"
        :return:
        '''
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
        a = cNote[name]
        return a


class _Note:
    '''
    这个类一般不允许其它文件使用。
    '''

    def __init__(self, note: cNote):
        self.note = note
        if not 1 <= self.note.value <= 12:
            raise ValueError("note index must be between 1 and 12")
        self.index = self.note.value

    '''
    "A" -> _Note(cNote.A)
    '''

    @staticmethod
    def init_by_note_name(name: str):
        return _Note(cNote.get_cNote_by_name(name))

    def __repr__(self):
        return "_Note--'{}'".format(self.name)

    @property
    def name(self):
        return self.note.name

    @property
    def angle(self):
        return self.index * 30 - 15

    def angle_to(self, other):
        return (self - other) * 30

    # 获取从self到other逆时针方向的纯五跨度数
    def __sub__(self, other) -> int:

        if not isinstance(other, _Note):
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

    # 返回逆时针方向第n个音符_Note

    def next(self, n=1):
        new_ind = self.index + n
        if n >= 0:
            if new_ind > 12:
                new_ind -= 12
        else:
            if new_ind <= 0:
                new_ind += 12

        return _Note(cNote(new_ind))


class Chord:

    def __init__(self, notes: list, name=None):
        if len(notes) == 0:
            raise "没有输入音符"
        self.name = name
        self.temp_theta = None

        notes = set(notes)  # 去除重复音符
        self.note_names = [i.name for i in notes]
        self.notes = []  # self.notes 存储音符_Note类实例的列表
        for i in notes:
            self.notes.append(_Note(i))
        self.notes.sort()
        self.keyboard_order = keyboard_order(notes)

    '''
    直接用音符名str获取和弦对象["C","E","G"]
    '''

    def init_by_note_name_str(notes: list, name=None):
        if len(notes) == 0:
            raise "没有输入音符"
        cNote_list = []
        for i in notes:
            cNote_list.append(cNote.get_cNote_by_name(i))
        return Chord(cNote_list, name)

    def __repr__(self):
        return f"Chord {self.name} ({', '.join([note.name for note in self.notes])})"

    """
    [_Note]->Chord
    从_Note类的列表初始化Chord
    """

    def initBy_Note(notes: list, name=None):
        if len(notes) == 0:
            raise "没有输入音符"
        cNote_list = []
        for i in notes:
            cNote_list.append(cNote.get_cNote_by_name(i.name))
        return Chord(cNote_list, name)

    def get_theta(self) -> list:
        # 计算和弦内音符对应向量的平均方向
        thetas = []
        intervals = []
        for i in range(len(self.notes)):
            intervals.append(self.notes[i] - self.notes[(i + 1) % len(self.notes)])
        max_interval = max(intervals)
        for i in range(len(intervals)):
            if (intervals[i] == max_interval):

                n_begin = self.notes[(i + 1) % len(self.notes)]
                theta = 0
                for n in self.notes:
                    theta += 30 * (n_begin - n)
                thetas.append((theta / len(self.notes) + n_begin.angle) % 360)
        if len(thetas) == 1:
            self.temp_theta = thetas[0]
        return thetas

    def pure_fifth_span(self) -> int:
        '''
        计算纯五跨度数
        :return: int
        '''
        intervals = []
        angles = list(i.index for i in self.notes)
        angles.sort()
        for i in range(len(angles) - 1):
            intervals.append(angles[i + 1] - angles[i])

        def f(x): return x + 12 * int((abs(x) != x))

        intervals.append(f(angles[0] - angles[-1]))
        max_ang = max(intervals)
        return 12 - max_ang

    def get_semitones(self) -> int:
        '''
        计算半音程数
        :return:
        '''
        count = 0
        for i in range(len(self.notes)):
            for j in range(i + 1, len(self.notes)):
                interval = self.notes[i] - self.notes[j]
                if interval == 5 or interval == 7:
                    count += 1
        return count

    def get_Major2nd(self) -> int:
        '''
        计算大二度数
        :return:
        '''
        count = 0
        for i in range(len(self.notes)):
            for j in range(i + 1, len(self.notes)):
                interval = self.notes[i] - self.notes[j]
                if interval == 2 or interval == 10:
                    count += 1
        return count

    def if_Major_Chord_exist(self) -> bool:
        '''
        是否存在大三和弦
        :return:
        '''

        for i in self.notes:
            _a = i.next(3)
            _b = i.next(4)
            aexist = False
            bexist = False
            for j in self.notes:
                if j == _a:
                    aexist = True
                if j == _b:
                    bexist = True
            if (aexist and bexist):
                return True
        return False

    def if_Minor_Chord_exist(self):
        '''
        是否存在小三和弦
        :return:
        '''
        for i in self.notes:
            _a = i.next(1)
            _b = i.next(4)
            aexist = False
            bexist = False
            for j in self.notes:
                if j == _a:
                    aexist = True
                if j == _b:
                    bexist = True
            if (aexist and bexist):
                return True
        return False

    def get_consecutive_semitones(self) -> int:
        '''
        计算连续半音程数
        :return: int
        '''
        sorted_order = self.keyboard_order
        subsets = find_ordered_subsets(sorted_order)

        for subset in subsets:
            if subset in possible_consecutive_semitones(4):
                return 4

        for subset in subsets:
            if subset in possible_consecutive_semitones(3):
                return 3

        for subset in subsets:
            if subset in possible_consecutive_semitones(2):
                return 2

        for subset in subsets:
            if subset in possible_consecutive_semitones(1):
                return 1

        return 0

    def get_harmony(self):
        '''
        获得向量模长
        :return:
        '''
        harmony = 1.77777
        perfect5 = self.pure_fifth_span()
        Major2 = self.get_Major2nd()
        Minor2 = self.get_semitones()
        Major = self.if_Major_Chord_exist()
        Minor = self.if_Minor_Chord_exist()
        Semis = self.get_consecutive_semitones()

        if perfect5 >= 2 and perfect5 <= 4 and Minor2 == 0:
            if Major2 <= 1:
                if (Major or Minor):
                    harmony = 10
                else:
                    harmony = 9.67
            if Major2 >= 2 and Major2 <= 3:
                harmony = 9.33
        elif perfect5 == 5 and Minor2 == 1:
            if Major2 <= 1 and (Major or Minor):
                harmony = 7
            elif Major2 == 2 and (Major or Minor):
                harmony = 6.67
            elif Major2 > 2 or not (Major or Minor):
                harmony = 6.33
        elif perfect5 == 6:
            if Minor2 == 0:
                if Major2 <= 1:
                    if (Major or Minor):
                        harmony = 9
                    else:
                        harmony = 8.67
                elif Major2 == 3:
                    harmony = 8.33
            elif Minor2 == 1:
                if Major2 == 1 and (Major or Minor):
                    harmony = 6
                elif Major2 == 2 and (Major or Minor):
                    harmony = 5.67
                elif Major2 >= 2 or not (Major or Minor):
                    harmony = 5.33
            elif Minor2 == 2:
                if Major2 == 1 and (Major or Minor):
                    harmony = 4
                elif Major2 >= 1 or not (Major or Minor):
                    harmony = 3.5
        elif perfect5 >= 7 and perfect5 <= 11:
            if (Minor2 == 0):
                if perfect5 == 8 and Major2 == 0:
                    harmony = 8
                elif perfect5 == 8 and Major2 == 2:
                    harmony = 7.67
                elif Major2 >= 2 or perfect5 > 8:
                    harmony = 7.33
            elif (Minor2 == 1):
                if Major2 == 0 and (Major or Minor):
                    harmony = 5
                elif Major2 <= 2 and (Major or Minor):
                    harmony = 4.67
                elif Major2 > 2 or not (Major or Minor):
                    harmony = 4.33
            elif (Minor2 == 2):
                if Major2 <= 2 and (Major or Minor):
                    harmony = 3
                elif Major2 >= 2 or not (Major or Minor):
                    harmony = 2.75
                elif Major2 <= 3 and (Major or Minor):
                    harmony = 2.5
                elif Major2 > 3 or not (Major or Minor):
                    harmony = 2.25
            elif (Minor2 == 3):
                if Semis <= 1:
                    harmony = 2.00
                elif Semis == 2:
                    harmony = 1.67
                elif Semis >= 3:
                    harmony = 1.33
            elif (Minor2 >= 4):
                if Semis <= 2:
                    harmony = 1.00
                elif Semis == 3:
                    harmony = 0.67
                elif Semis >= 4:
                    harmony = 0.33
        else:
            pass
        return harmony

    def get_coordinates(self, method='r_theta') -> tuple:
        '''
        获得和弦极坐标或直角坐标，有多个可能角度的和弦选取最小角
        '''
        r = self.get_harmony()
        theta = min(self.get_theta())

        if method == 'r_theta':
            return (r, theta)
        elif method == 'x_y':
            angle = math.radians(theta)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            return (x, y)
        else:
            print('Method does not exist, using default method r_theta.')
            return (r, theta)

    @staticmethod
    def angle_diff(a1, a2):
        diff = abs(a1 - a2) % 360
        return diff if diff <= 180 else 360 - diff

    @staticmethod
    def get_color_change(chord1, chord2):
        angle1 = 0
        angle2 = 0
        if chord1.temp_theta != None and chord2.temp_theta != None:
            angle2 = chord2.temp_theta
            angle1 = chord1.temp_theta
        elif chord1.temp_theta != None and chord2.temp_theta == None:
            angle1 = chord1.temp_theta
            mintheta = 6999
            for i in chord2.get_theta():
                if Chord.angle_diff(i, angle1) < mintheta:
                    mintheta = Chord.angle_diff(i, angle1)
                    angle2 = i
        elif chord2.temp_theta != None and chord1.temp_theta == None:
            angle2 = chord2.temp_theta
            mintheta = 9999
            for i in chord1.get_theta():
                if Chord.angle_diff(i, angle2) < mintheta:
                    mintheta = Chord.angle_diff(i, angle2)
                    angle1 = i
        else:
            mintheta = 9999
            for i in chord1.get_theta():
                for j in chord2.get_theta():
                    if Chord.angle_diff(i, j) < mintheta:
                        angle1 = i
                        angle2 = j
        r1 = chord1.get_harmony()
        r2 = chord2.get_harmony()
        # 将角度转换为弧度
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)

        # 计算两个点的x, y坐标
        x1 = r1 * math.cos(angle1)
        y1 = r1 * math.sin(angle1)
        x2 = r2 * math.cos(angle2)
        y2 = r2 * math.sin(angle2)

        # 计算距离
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    @staticmethod
    def get_tension_change(chord1, chord2):
        return abs(chord2.get_harmony() - chord1.get_harmony())

    @staticmethod
    def get_fressness(chord1, chord2):
        return Chord.get_tension_change(chord1, chord2) + Chord.get_color_change(chord1, chord2)

    '''
    返回一个新的Chord实例，把self的所有音符在五度圈上逆时针旋转n*30°
    '''

    def rotate(self, n: int, new_name: str = None):
        new_notes = []
        for i in self.notes:
            new_notes.append(i.next(n))
        return Chord.initBy_Note(new_notes, new_name)


def all_chord_coordinates(n_notes=[3, 4], method='r_theta') -> dict:
    '''
    获得全部可能的和弦及其坐标
    '''
    notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
    temp = []
    if type(n_notes) == int:
        n_notes = [n_notes]

    chords = dict()
    for i in n_notes:
        temp += combinations(notes, i)
    for ls in temp:
        chord = Chord.init_by_note_name_str(ls)
        chords[chord] = chord.get_coordinates(method=method)

    return chords


def find_ordered_subsets(my_list) -> list:
    '''
    寻找一个tuple按顺序不重复的子集
    '''
    subsets = []
    for i in range(len(my_list)):
        for j in range(i + 1, len(my_list) + 1):
            subsets.append(my_list[i:j])
    return subsets


def keyboard_order(notes: list) -> list:
    '''
    将notes映射为键盘顺序，以C为起始
    '''
    keyboard_order = {
        cNote.C: 1,
        cNote.Db: 2,
        cNote.D: 3,
        cNote.Eb: 4,
        cNote.E: 5,
        cNote.F: 6,
        cNote.Fsharp: 7,
        cNote.G: 8,
        cNote.Ab: 9,
        cNote.A: 10,
        cNote.Bb: 11,
        cNote.B: 12,
    }

    sorted_order = sorted(keyboard_order[note] for note in notes)
    return sorted_order


def possible_consecutive_semitones(n: int) -> list:
    '''
    按键盘顺序的所有可能连续半音程的组合
    '''
    semitones = []
    for i in range(1, 13):
        temp = tuple(range(i, i + n + 1))
        semitone = sorted([num - 12 if num > 12 else num for num in temp])
        if semitone not in semitones:
            semitones.append(semitone)

    return semitones