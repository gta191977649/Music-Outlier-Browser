import matplotlib.pyplot as plt

# Create a figure and axes
fig, ax = plt.subplots()

# Set the font name for the tick labels
font = {'family': 'Arial', 'size': 14}
ax.set_ticklabels(ax.get_xticklabels(), font)
ax.set_ticklabels(ax.get_yticklabels(), font)

# Plot the data and show the plot
ax.plot([1, 2, 3], [4, 5, 6])
plt.show()