import numpy as np
import scipy
import matplotlib.pyplot as plt
import librosa
import libfmp.b
import libfmp.c3
import libfmp.c4
from chordify.feature_extractor import *
import os

class Chordify:
    def __init__(self, file):
        self.file = file
        self.chord_template = self.generate_chord_templates()
        # process
        fn_wav = os.path.join('../music/love_is_in_the_air.mp3')
        N = 4096
        H = 2048

        X_STFT, Fs_X, x, Fs, x_dur = compute_chromagram_from_filename(fn_wav, N=N, H=H, gamma=0.1, version='STFT')

        # Chord recognition
        X = X_STFT
        chord_sim, chord_max = self.chord_recognition_template(X, norm_sim='max')
        chord_labels = self.get_chord_labels(nonchord=False)
        X_chord = np.matmul(self.chord_template, chord_max)

        # Plot
        # cmap = libfmp.b.compressed_gray_cmap(alpha=1, reverse=False)

        fig, ax = plt.subplots(4, 2, gridspec_kw={'width_ratios': [1, 0.03],
                                                  'height_ratios': [1.5, 3, 3, 0.3]}, figsize=(8, 10))
        libfmp.b.plot_chromagram(X, ax=[ax[0, 0], ax[0, 1]], Fs=Fs_X, clim=[0, 1], xlabel='',
                                 title='STFT-based chromagram (feature rate = %0.1f Hz)' % (Fs_X))


        libfmp.b.plot_matrix(chord_sim, ax=[ax[1, 0], ax[1, 1]], Fs=Fs_X,
                             title='Time–chord representation of chord similarity matrix',
                             ylabel='Chord', xlabel='')
        ax[1, 0].set_yticks(np.arange(len(chord_labels)))
        ax[1, 0].set_yticklabels(chord_labels)


        libfmp.b.plot_matrix(X_chord, ax=[ax[2, 0], ax[2, 1]], Fs=Fs_X,
                             title='Time–chord representation of chord recognition result',
                             ylabel='Chord', xlabel='')
        ax[2, 0].set_yticks(np.arange(len(chord_labels)))
        ax[2, 0].set_yticklabels(chord_labels)
        ax[2, 0].grid()


        ax[3, 1].axis('off')
        plt.tight_layout()

        plt.show()



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

    def chord_recognition_template(self,X, norm_sim='1', nonchord=False):
        """Conducts template-based chord recognition
        with major and minor triads (and possibly nonchord)

        Notebook: C5/C5S2_ChordRec_Templates.ipynb

        Args:
            X (np.ndarray): Chromagram
            norm_sim (str): Specifies norm used for normalizing chord similarity matrix (Default value = '1')
            nonchord (bool): If "True" then add nonchord template (Default value = False)

        Returns:
            chord_sim (np.ndarray): Chord similarity matrix
            chord_max (np.ndarray): Binarized chord similarity matrix only containing maximizing chord
        """
        chord_templates = self.generate_chord_templates(nonchord=nonchord)
        X_norm = normalize_feature_sequence(X, norm='2')
        chord_templates_norm = normalize_feature_sequence(chord_templates, norm='2')
        chord_sim = np.matmul(chord_templates_norm.T, X_norm)
        if norm_sim is not None:
            chord_sim = normalize_feature_sequence(chord_sim, norm=norm_sim)
        # chord_max = (chord_sim == chord_sim.max(axis=0)).astype(int)
        chord_max_index = np.argmax(chord_sim, axis=0)
        chord_max = np.zeros(chord_sim.shape).astype(np.int32)
        for n in range(chord_sim.shape[1]):
            chord_max[chord_max_index[n], n] = 1

        return chord_sim, chord_max

    def get_chord_labels(self,ext_minor='m', nonchord=False):
        """Generate chord labels for major and minor triads (and possibly nonchord label)

        Notebook: C5/C5S2_ChordRec_Templates.ipynb

        Args:
            ext_minor (str): Extension for minor chords (Default value = 'm')
            nonchord (bool): If "True" then add nonchord label (Default value = False)

        Returns:
            chord_labels (list): List of chord labels
        """
        chroma_labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chord_labels_maj = chroma_labels
        chord_labels_min = [s + ext_minor for s in chroma_labels]
        chord_labels = chord_labels_maj + chord_labels_min
        if nonchord is True:
            chord_labels = chord_labels + ['N']
        return chord_labels

    def plot_chromagram_annotation(self,ax, X, Fs_X, ann, color_ann, x_dur, cmap='gray_r', title=''):
        """
        Plot chromagram and annotation

        Notebook: C5/C5S2_ChordRec_Templates.ipynb

        Args:
            ax: Axes handle
            X: Feature representation
            Fs_X: Feature rate
            ann: Annotations
            color_ann: Color for annotations
            x_dur: Duration of feature representation
            cmap: Color map for imshow (Default value = 'gray_r')
            title: Title for figure (Default value = '')
        """
        libfmp.b.plot_chromagram(X, Fs=Fs_X, ax=ax,
                                 chroma_yticks=[0, 4, 7, 11], clim=[0, 1], cmap=cmap,
                                 title=title, ylabel='Chroma', colorbar=True)
        libfmp.b.plot_segments_overlay(ann, ax=ax[0], time_max=x_dur,
                                       print_labels=False, colors=color_ann, alpha=0.1)

if __name__ == '__main__':
    c = Chordify("../music/AKB48_kiminomelody.mp3")