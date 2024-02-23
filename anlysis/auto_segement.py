import allin1

if __name__ == '__main__':
    result = allin1.analyze(
        '/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe_aud/wav/Europe - The Final Countdown (Official Video) [9jK-NcRmVcw].mp3',device="cpu")
    print(result)
    fig = allin1.visualize(result)
    fig.show()