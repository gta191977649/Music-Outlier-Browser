from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.features.key import CNNKeyRecognitionProcessor,key_prediction_to_label


class Chordify:
    def __init__(self,file):
        self.file =file

    def anlysis(self):
        dcp = DeepChromaProcessor()
        decode = DeepChromaChordRecognitionProcessor()
        chroma = dcp(self.file)
        chords = decode(chroma)
        return chords
    def getLabFile(self,chords):
        lab_file = ""
        for chord in chords:
            start, end, name = chord
            print(start, end, name)
            lab_file += "{}\t{}\t{}\n".format(start, end, name)
        return  lab_file
        # f = open(PATH + ".lab", "w")
        # f.write(lab_file)
        # f.close()
