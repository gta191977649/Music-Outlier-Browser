import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class PlotChordTransition:
    def __init__(self,title = "Chord Transition"):
        self.title = title
        self.circle_of_fifths_maj = ['Cmaj', 'Gmaj', 'Dmaj', 'Amaj', 'Emaj', 'Bmaj', 'F#maj', 'C#maj', 'Abmaj', 'Ebmaj',
                                     'Bbmaj', 'Fmaj']
        self.circle_of_fifths_minor = ['Cmin', 'Gmin', 'Dmin', 'Amin', 'Emin', 'Bmin', 'F#min', 'C#min', 'Abmin',
                                       'Ebmin', 'Bbmin', 'Fmin']
        self.enharmonic_map = {
            'G#maj': 'Abmaj',
            'G#min': 'Abmin',
            'D#maj': 'Ebmaj',
            'D#min': 'Ebmin',
            'A#maj': 'Bbmaj',
            'A#min': 'Bbmin',
            'C#maj': 'Dbmaj',
            'C#min': 'Dbmin',
            'Gbmaj': 'F#maj',
            'F#min': 'Gbmin',
        }
        self.circle_of_fifths = self.circle_of_fifths_maj + self.circle_of_fifths_minor
        self.node_pos = {}
        self.node_distance = 2
        self.node_inner_distance = 1.6
        self.chord_node = nx.DiGraph()

        # Initialize node positions
        self.initialize_node_positions()

    def initialize_node_positions(self):
        # Initialize positions for major chords in the outer circle
        for i, key in enumerate(self.circle_of_fifths_maj):
            angle = 2 * np.pi * i / len(self.circle_of_fifths_maj)  # Evenly space nodes around the circle
            self.node_pos[key] = (self.node_distance * np.cos(angle), self.node_distance * np.sin(angle))
            self.chord_node.add_node(key)

        # Initialize positions for minor chords in the inner circle
        for i, key in enumerate(self.circle_of_fifths_minor):
            angle = 2 * np.pi * i / len(self.circle_of_fifths_minor)  # Evenly space nodes around the circle
            self.node_pos[key] = (self.node_inner_distance * np.cos(angle), self.node_inner_distance * np.sin(angle))
            print(key)
            self.chord_node.add_node(key)

    def addChordTransition(self, a, b):
        a, b = self.handle_enharmonic(a), self.handle_enharmonic(b)
        if not self.chord_node.has_edge(a, b):
            self.chord_node.add_edge(a, b, weight=0.1)
        else:
            self.chord_node[a][b]['weight'] += 0.1  # Increase weight for repeated transitions


    def handle_enharmonic(self, chord):
        mapped_chord = self.enharmonic_map.get(chord, chord)  # Map chord to its enharmonic equivalent if exists
        # Check if the mapped chord exists in the major or minor lists
        if mapped_chord in self.circle_of_fifths_maj or mapped_chord in self.circle_of_fifths_minor:
            return mapped_chord
        else:
            # If the mapped chord doesn't exist, check if the original chord does
            if chord in self.circle_of_fifths_maj or chord in self.circle_of_fifths_minor:
                return chord
            else:
                # Handle the case where neither the mapped nor the original chord exists
                print(f"Warning: Chord {chord} (mapped to {mapped_chord}) does not exist in the defined circles.")
                return None  # or handle differently as needed

    def draw_graph(self, G, node_pos, edge_color, title):
        nx.draw_networkx_nodes(G, node_pos, node_color='w', edgecolors='black', node_size=1800)
        nx.draw_networkx_labels(G, node_pos)
        edge_widths = [G[u][v]['weight'] for u, v in G.edges()]
        nx.draw_networkx_edges(G, node_pos, width=edge_widths, edge_color=edge_color, arrowsize=20)
        plt.title(self.title)

    def showPlot(self):
        plt.figure(figsize=(8, 8))  # Set the figure size
        self.draw_graph(self.chord_node, self.node_pos, 'blue', 'Major Chord Transitions')
        plt.tight_layout()
        plt.axis('off')
        plt.gca().set_aspect('equal', adjustable='box')  # Keep the aspect ratio circular
        plt.show()
