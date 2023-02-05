import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

x = [1, 2, 3]
y = [1, 2, 3]
group = [0, 1, 0]

# Create a scatterplot
plt.scatter(x, y, c=group, cmap='viridis')

# Create a kdeplot
sns.kdeplot(np.array(x), np.array(y), cmap='viridis', n_levels=5, c=group)

plt.show()