import pandas as pd
if __name__ == '__main__':
    csv_info = pd.read_csv('/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/id_information.csv'
                           ,delimiter="\t")
    csv_meta = pd.read_csv('/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/id_metadata.csv'
                           ,delimiter="\t")
    csv_tag = pd.read_csv('/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/id_tags.csv'
                          ,delimiter="\t")

    merged_df = pd.merge(csv_info, csv_meta, on='id', how='inner')

    # Then merge the result with csv_tag on 'id'
    final_merged_df = pd.merge(merged_df, csv_tag, on='id', how='inner')

    final_merged_df = final_merged_df.sort_values(by=['release'])
    # Display the first few rows of the final merged DataFrame (optional)
    print(final_merged_df.head())

    final_merged_df.to_csv("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/music4all/dataset.csv", index=False)