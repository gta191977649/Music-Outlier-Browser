import os.path
import numpy as np
import vendor.hdf5.hdf5_getters as hdf5_getters
from sklearn.model_selection import KFold
import pandas as pd
import dataset as data
import plot as plot
from tslearn.metrics import dtw_path
import groundtruth as gt
from sklearn.metrics import f1_score
import allin1
import song as songUtils
def processSong(path):
    # 1.Pre-processing
    song = data.getData(path)
    section_features = data.getSectionFeature(song, feature="loudness")

    # 2.Model section constrast by DTW
    contrast_matrix = []
    for i in range(0, len(section_features) - 1):
        #plot.plotDTW(section_features[i],section_features[i+1])
        path, sim = dtw_path(section_features[i]["feature"], section_features[i + 1]["feature"])
        contrast_matrix.append(sim)
    # 3.Aggregate Scores
    aggregated_score = np.mean(contrast_matrix)
    return aggregated_score, contrast_matrix


def envaluate(outliers):
    csv = pd.read_csv("../dataset/outlier/ground_truth.csv")
    groundTruth = gt.getDataByArtist(csv, "Colin Meloy")

    groundTruth_binary = [1 if song['Outlier'] == 1.0 else 0 for song in groundTruth]
    predicted_binary = [1 if song['Title'] in outliers else 0 for song in groundTruth]

    # Calculate F1 Score
    f1 = f1_score(groundTruth_binary, predicted_binary)

    print("--------------")
    print("F1 Score:", f1, "{}".format(f1 < 50 and "☹️" or "🎉"))
    return f1


def detectSection(path):
    #result = allin1.analyze(path,out_dir="./",device="mps")
    result = allin1.analyze(path,device="cuda")
    sections = []
    for idx,section in enumerate(result.segments):
        sections.append({
            "id":idx,
            "start":section.start,
            "end":section.end,
            "label":section.label
        })

    return sections

def seconds_to_mm_ss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return "{:02d}:{:02d}".format(minutes, seconds)


if __name__ == '__main__':
    # result = detectSection('../music/title.mp3')
    # print(result)
    # fig = allin1.visualize(result)
    # fig.show()

    # 1. Prepare data
    ARTIST_NAME = "colin_meloy"
    songs = []
    for idx, filename in enumerate(os.listdir("../data/{}/".format(ARTIST_NAME))):
        full_file_path = os.path.join("../data/{}/".format(ARTIST_NAME), filename)
        if os.path.exists(full_file_path):
            file = hdf5_getters.open_h5_file_read(full_file_path)
            section_features = data.getSectionFeature(file, feature="loudness")
            score,sections_contrasts = processSong(full_file_path)

            contrasts = np.array(sections_contrasts)
            if contrasts.size == 0:
                max_section = None  # or set a default value
            else:
                max_section = np.argmax(contrasts)

            song = {
                "file":file,
                "id": hdf5_getters.get_song_id(file),
                "title": hdf5_getters.get_title(file),
                "score": score,
                "contrast_matrix":sections_contrasts,
                "max_section":max_section
            }
            if not np.isnan(song["score"]):
                songs.append(song)

    # 2. Normalize DTW Scores
    scores = [song["score"] for song in songs]

    # Normalize the scores using min-max normalization
    min_score = min(scores)
    max_score = max(scores)
    normalized_scores = [(score - min_score) / (max_score - min_score) for score in scores]

    # Update the 'score' key in the songs list with the normalized scores
    for song, norm_score in zip(songs, normalized_scores):
        song["score"] = norm_score


    # 3. Detect outliers
    Q1 = np.percentile(normalized_scores, 25)
    Q3 = np.percentile(normalized_scores, 75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Generate outliers
    outliers = [song for song in songs if song["score"] < lower_bound or song["score"] > upper_bound]

    # Print out the song IDs of the outliers
    for outlier in outliers:
        print(outlier["id"],outlier["title"],outlier["score"],outlier["contrast_matrix"])
    # Print Average Score for dist
    print("Mean Score: ",np.mean(normalized_scores))

    # 4. Testing Results
    envaluate(outliers)

    # 5. Print out most section pairs that has max contrast in time frame
    for outlier in outliers:
        file = outlier["file"]
        max_contribute_section_index = outlier["max_section"],
        index = max_contribute_section_index[0]
        # get most contribute
        section_features = data.getSectionFeature(file, feature="loudness")
        print("Name: {}, start: {}, end: {}".format(outlier["title"],seconds_to_mm_ss(section_features[index]["time"][0]),seconds_to_mm_ss(section_features[index]["time"][1])))

    # Visualize the outlier songs
    plot.plot_histogram_and_bars(songs,outliers)
