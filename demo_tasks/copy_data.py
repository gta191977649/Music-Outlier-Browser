import os
import shutil

def find_and_copy_files(src_path, dest_folder="dataset"):
    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Read filenames from artilst_datalist.txt
    with open("artilst_datalist.txt", "r") as f:
        filenames = [line.strip() + ".h5" for line in f]

    # Walk through the source path and its subdirectories
    for dirpath, _, files in os.walk(src_path):
        for file in files:
            for target_file in filenames:
                if target_file == file:
                    src_file_path = os.path.join(dirpath, file)
                    # Specify the filename directly in the destination path
                    dest_file_path = os.path.join(dest_folder, target_file)
                    shutil.copy2(src_file_path, dest_file_path)
                    print(f"Copied {file} to {dest_folder}")

if __name__ == "__main__":
    find_and_copy_files(src_path="/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/MSD",\
                        dest_folder="/Users/nurupo/Desktop/dev/Music-Outlier-Browser/dataset/file")
