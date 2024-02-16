from chordify import feature_extractor as feature
import os
import pandas as pd
import hashlib

def getFileHash(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()
def generateDatasetMetaFile(base_path,output_path):

    id_ls = []
    title_ls = []
    key_ls = []
    mode_ls = []
    time_sig_ls = []
    tempo_ls = []
    for root, dirs, files in os.walk(base_path):
        for idx, filename in enumerate(files):
            fullpath = os.path.join(root, filename)
            title = fullpath.split('/')[-1]
            print(title)
            id = getFileHash(fullpath)
            id_ls.append(id)
            title_ls.append(title)
            key_parts,_ = feature.extract_feature(fullpath,feature="key")
            tempo = feature.extract_feature(fullpath,feature="tempo")
            key_parts = key_parts.split(" ")
            key = key_parts[0]
            mode = key_parts[1]
            key_ls.append(key)
            mode_ls.append(mode)
            tempo_ls.append(tempo)
    df = pd.DataFrame({
        "id": id_ls,
        "title": title_ls,
        "key": key_ls,
        "mode": mode_ls,
        "tempo": tempo_ls,
        "time_signature": 4,
    })
    df.to_csv(output_path,index=False)
    print(df)



if __name__ == '__main__':
    generateDatasetMetaFile("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe_aud/wav","/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe_aud/meta.csv")