import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
csv_info_path = '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/dataset.csv'
csv_info = pd.read_csv(csv_info_path, delimiter=',')

# Ensure 'release' is treated as an integer
csv_info['release'] = csv_info['release'].astype(int)

# Group by 'release' year and count unique artists
artists_per_year = csv_info.groupby('release')['artist'].nunique()

# Plotting
plt.figure(figsize=(5, 3))
sns.lineplot(x=artists_per_year.index, y=artists_per_year.values, color="red")
plt.title('Number of Artists vs. Year', fontsize=14, fontname='MSGothic')
plt.xlabel('Year', fontsize=12, fontname='MSGothic')
plt.ylabel('Number of Artists', fontsize=12, fontname='MSGothic')
plt.xticks(rotation=45, fontname='MSGothic')
plt.yticks(fontname='MSGothic')
plt.grid(True)

plt.tight_layout()
plt.show()