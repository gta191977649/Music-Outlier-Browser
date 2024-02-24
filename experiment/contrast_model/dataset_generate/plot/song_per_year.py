import pandas as pd

csv_info_path = '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/dataset.csv'
csv_info = pd.read_csv(csv_info_path, delimiter=',')

csv_info['release'] = csv_info['release'].astype(int)

songs_per_year = csv_info.groupby('release').size().reset_index(name='number_of_songs')

output_csv_path = '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/songs_per_year.csv'
songs_per_year.to_csv(output_csv_path, index=False)

print(f"The number of songs per year has been saved to {output_csv_path}")
