from chordify import feature_extractor as feature

if __name__ == '__main__':
    feature = feature.extract_feature("/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe_aud/wav/The Final Countdown [NNiTxUEnmKI].mp3","key")
    print(feature)