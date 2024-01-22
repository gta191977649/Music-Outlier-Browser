import numpy as np
import scipy
import matplotlib.pyplot as plt

import librosa
class Chordify:
    def __init__(self, file):
        self.file = file
        self.templte = self.generate_chord_templates()

    def generate_chord_templates(self,nonchord=False):
        """Generate chord templates of major and minor triads (and possibly nonchord)

        Notebook: C5/C5S2_ChordRec_Templates.ipynb

        Args:
            nonchord (bool): If "True" then add nonchord template (Default value = False)

        Returns:
            chord_templates (np.ndarray): Matrix containing chord_templates as columns
        """
        template_cmaj = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]).T
        template_cmin = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]).T
        num_chord = 24
        if nonchord:
            num_chord = 25
        chord_templates = np.ones((12, num_chord))
        for shift in range(12):
            chord_templates[:, shift] = np.roll(template_cmaj, shift)
            chord_templates[:, shift+12] = np.roll(template_cmin, shift)
        return chord_templates

if __name__ == '__main__':
    c = Chordify("../music/AKB48_kiminomelody.mp3")