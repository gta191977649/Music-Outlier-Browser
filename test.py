import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import scrolledtext

def on_pick(event):
    # Get the x and y data for the point that was clicked
    x, y = event.artist.get_offsets()[event.ind[0]]
    text.insert(tk.INSERT, f"You clicked on point ({x:.2f}, {y:.2f})\n")
    root.deiconify()

# Generate some random data to plot
np.random.seed(0)
x = np.random.rand(100)
y = np.random.rand(100)

# Create the Matplotlib plot
fig, ax = plt.subplots()
scatter = ax.scatter(x, y)
fig.canvas.mpl_connect("pick_event", on_pick)

# Create the Tkinter GUI
root = tk.Tk()
root.iconify() # minimize the GUI
root.title("Matplotlib Clicked Event Example")

text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text.pack(fill=tk.BOTH, expand=True)

plt.show()
