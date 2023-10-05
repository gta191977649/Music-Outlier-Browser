import pandas as pd
def getGroundTruthOutliersByArtist(csv,artist):
    filtered_data = csv[(csv['Artist'] == artist) & (csv['Outlier'] == 1.0)]
    final_list = filtered_data.to_dict(orient='records')
    return final_list
def getDataByArtist(csv,artist):
    filtered_data = csv[(csv['Artist'] == artist)]
    final_list = filtered_data.to_dict(orient='records')
    return final_list
