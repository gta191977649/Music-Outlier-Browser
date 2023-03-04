import matplotlib.pyplot as plt
import numpy as np

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot the data with a colormap
sc = plt.scatter(x, y, c=y, cmap='coolwarm')

# Add a colorbar
cb = plt.colorbar(sc)
cb.set_label('y')
plt.legend()
# Show the plot
plt.show()