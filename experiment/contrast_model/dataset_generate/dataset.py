import os
import pandas as pd
import hashlib
from chordify import feature_extractor as feature
from multiprocessing import Pool, cpu_count
from pychord.constants import NOTE_VAL_DICT


INDEX_NOTE_DICT = {v: k for k, v in NOTE_VAL_DICT.items()}


def write_chord_file(filename,chords,beats):
    chordsArray = []
    chord_idx = 0
    lab_file_path = filename
    for beat_idx in range(len(beats) - 1):
        curr_beat_time, curr_beat = beats[beat_idx]
        # find the corresponding chord for this beat
        while chord_idx < len(chords):
            chord_time, _, _ = chords[chord_idx]
            prev_beat_time, _ = (0, 0) if beat_idx == 0 else beats[beat_idx - 1]
            eps = (curr_beat_time - prev_beat_time) / 2
            if chord_time > curr_beat_time + eps:
                break
            chord_idx += 1

        # append to array
        _, _, prev_chord = chords[chord_idx - 1]
        chord = (curr_beat_time, curr_beat, prev_chord)

        chordsArray.append(chord)

    # Generate chord label file
    lab_file = ""
    for c in chordsArray:
        curr_beat_time, curr_beat, prev_chord = c
        print(curr_beat_time, curr_beat, prev_chord)
        lab_file += "{}\t{}\t{}\n".format(curr_beat_time, curr_beat, prev_chord)

    bts = []
    for b in beats:
        bts.append(b[0])

    f = open(lab_file_path , "w")
    f.write(lab_file)
    f.close()

    print("✅Processed: {}".format(filename))
def getFileHash(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()

def process_file(file_info):
    base_path, filename = file_info
    fullpath = os.path.join(base_path, filename)
    file_id = getFileHash(fullpath)
    try:
        key_parts, _ = feature.extract_feature(fullpath, feature="key")
        tempo = feature.extract_feature(fullpath, feature="tempo")
        key_parts = key_parts.split(" ")
        key = key_parts[0]
        mode = key_parts[1]
        return file_id, filename, key, mode, tempo
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return file_id, filename, "Error", "Error", "Error"

def generateDatasetMetaFile(base_path):
    base_path = os.path.join(base_path,"wav")
    output_path = os.path.join(base_path)
    files = [(root, filename) for root, dirs, filenames in os.walk(base_path) for filename in filenames]
    total_files = len(files)
    print(f"Total files to process: {total_files}")

    results = []
    with Pool(processes=cpu_count()) as pool:
        for i, result in enumerate(pool.imap_unordered(process_file, files), 1):
            results.append(result)
            print(f"Processed {result[1]} - {total_files - i} files left")

    if results:
        id_ls, title_ls, key_ls, mode_ls, tempo_ls = zip(*results)
        df = pd.DataFrame({
            "id": id_ls,
            "title": title_ls,
            "key": key_ls,
            "mode": mode_ls,
            "tempo": tempo_ls,
            "time_signature": [4]*len(id_ls),  # Assuming time_signature is 4 for all
        })
        df.to_csv(output_path+".csv", index=False)
        print(f"\nFinished processing all files. Results saved to {output_path}.")
    else:
        print("No files were processed. Check if the provided paths are correct and if the files are accessible.")

def process_chord_file(args):
    audio_path, chord_path, file_title = args
    audio_file = os.path.join(audio_path, file_title)
    if os.path.exists(audio_file):
        chords, beats = feature.extract_chord(audio_file)
        filename = file_title.replace(".mp3", ".lab")
        chord_file_name = os.path.join(chord_path, filename)
        write_chord_file(chord_file_name, chords, beats)
        return f"Processed {file_title}"
    else:
        return f"File {file_title} does not exist."


def generateChordFile(basePath):
    chord_path = os.path.join(basePath, "chord")
    audio_path = os.path.join(basePath, "wav")
    meta_file = os.path.join(basePath, "meta.csv")

    if not os.path.exists(meta_file):
        print("Meta file does not exist")
        return

    if not os.path.exists(chord_path):
        os.makedirs(chord_path)

    print("START DETECTING CHORDS ...")
    files = pd.read_csv(meta_file)
    files_left = len(files)  # Initialize files_left with the total number of files

    args_list = [(audio_path, chord_path, file["title"]) for index, file in files.iterrows()]

    with Pool(cpu_count()) as pool:
        # Submit all tasks and collect AsyncResult objects
        results = [pool.apply_async(process_chord_file, args=(args,)) for args in args_list]

        # Wait for each result and print progress
        for i, result in enumerate(results):
            print(result.get())  # This blocks until the result is ready
            files_left -= 1
            print(f"{files_left} FILE(S) LEFT")

        pool.close()
        pool.join()

    print("ALL DONE.")

if __name__ == '__main__':
    BASE_PATH = "/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/data/europe_aud"
    #generateDatasetMetaFile(BASE_PATH)
    #generateChordFile(BASE_PATH)
