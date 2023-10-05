import pandas as pd


def convert_csv(input_path, output_path):
    # Load the dataset
    data = pd.read_csv(input_path)

    # Forward fill the Artist column to associate each song with its artist
    data['Artist'] = data['Artist'].ffill()

    # Drop rows where Song is NaN, as they only contain the artist's name
    data_cleaned = data.dropna(subset=['Song'])

    # Drop any unnecessary columns (like 'Unnamed: 4')
    data_cleaned = data_cleaned.drop(columns=[col for col in data_cleaned.columns if 'Unnamed' in col])

    # Rename columns to the desired format
    data_cleaned.columns = ['Artist', 'Title', 'Outlier', 'Category']

    # Save the cleaned data to the specified output CSV file
    data_cleaned.to_csv(output_path, index=False)
    print("saved")


# Example usage
input_path = './outlier/artist_outlier_ground_truth.csv'
output_path = './outlier/ground_truth.csv'
convert_csv(input_path, output_path)
