import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load the dataset
csv_info_path = '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/dataset.csv'
csv_info = pd.read_csv(csv_info_path, delimiter=',')

# Ensure 'release' is an integer to handle years correctly
csv_info['release'] = csv_info['release'].astype(int)

# Group by 'release' year and count the number of songs
songs_per_year = csv_info.groupby('release').size()


# Plotting
plt.figure(figsize=(5, 3))
sns.lineplot(x=songs_per_year.index, y=songs_per_year.values,color="blue")
plt.title('Distribution of Number of Songs vs. Year')
plt.xlabel('Year')
plt.ylabel('Number of Songs')
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
