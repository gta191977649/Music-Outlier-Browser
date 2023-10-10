# Song Related Functions
from vendor.hdf5 import hdf5_getters
import dataset as data
from tslearn.metrics import dtw_path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.ticker import FuncFormatter

def seconds_to_mm_ss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return "{:02d}:{:02d}".format(minutes, seconds)

class Song:
    def __init__(self,path,feature="loudness"):
        self.inspect_feature = feature
        self.file = hdf5_getters.open_h5_file_read(path)
        self.id = hdf5_getters.get_song_id(self.file)
        self.title = hdf5_getters.get_title(self.file)
        self.artist = hdf5_getters.get_artist_name(self.file)
        self.section_features = data.getSectionFeature(self.file, feature=self.inspect_feature)
        self.score, self.sections_contrasts = self.modelContrast(path)
        self.max_section = np.argmax(self.sections_contrasts)
    def modelContrast(self,path):
        # 1.Pre-processing
        song = data.getData(path)
        section_features = data.getSectionFeature(song, feature=self.inspect_feature)

        # 2.Model section constrast by DTW
        contrast_matrix = []
        for i in range(0, len(section_features) - 1):
            path, sim = dtw_path(section_features[i]["feature"], section_features[i + 1]["feature"])
            contrast_matrix.append(sim)
        # 3.Aggregate Scores
        aggregated_score = np.mean(contrast_matrix)
        return aggregated_score, contrast_matrix

    def plot(self,showLegend=True):
        # Function to format time in seconds to mm:ss format
        def format_func(value, tick_number):
            minutes = int(value // 60)
            seconds = int(value % 60)
            return "{:02d}:{:02d}".format(minutes, seconds)

        fig, axs = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios': [3, 1]})

        # Get the Set1 colormap colors
        colors = plt.cm.Set1(np.linspace(0, 1, len(self.section_features)))

        # Plotting each section's loudness signal on the top subplot
        for idx, section in enumerate(self.section_features):
            # Deal with > 2 dim array (if any, just normalize it using its mean)
            if len(section["feature"].shape) > 1:
                section["feature"] = np.mean(section["feature"], axis=-1)

            times = np.linspace(section["time"][0], section["time"][1], len(section["feature"]))
            start_time_str = format_func(section["time"][0], None)
            end_time_str = format_func(section["time"][1], None)
            axs[0].plot(times, section["feature"], color=colors[idx],
                        label=f"Section: {start_time_str} to {end_time_str}", alpha=0.8)

        axs[0].set_title('{}\n{} over Time'.format(self.title, self.inspect_feature))
        axs[0].set_xlabel('Time (mm:ss)')
        axs[0].set_ylabel(self.inspect_feature)
        axs[0].grid(True)
        if showLegend:
            axs[0].legend()

        # Plotting the contrasts between sections on the bottom subplot
        max_contrast_index = np.argmax(self.sections_contrasts)
        mid_times = []
        for idx, section in enumerate(self.section_features[:-1]):
            start_time = section["time"][1]
            end_time = self.section_features[idx + 1]["time"][0]
            mid_time = (start_time + end_time) / 2
            mid_times.append(mid_time)

        axs[1].plot(mid_times, self.sections_contrasts, color='black', zorder=1, label="Contrast Values", linewidth=1.5,alpha=0.8)
        for idx, (mid_time, contrast) in enumerate(zip(mid_times, self.sections_contrasts)):
            color = 'red' if idx == max_contrast_index else 'black'
            axs[1].scatter(mid_time, contrast, color=color, s=50, zorder=2)
            offset = mtransforms.offset_copy(axs[1].transData, fig=fig, y=5, units='points')
            axs[1].text(mid_time, contrast, f"{contrast:.1f}", fontsize=10, ha='center', va='bottom', color=color,
                        transform=offset)

        axs[1].set_title('DTW Contrasts over Time')
        axs[1].set_xlabel('Time (mm:ss)')
        axs[1].set_ylabel('DTW Contrast')
        axs[1].grid(True)
        if showLegend:
            axs[1].legend()


        # Adding vertical lines to indicate which sections are being compared
        for idx, mid_time in enumerate(mid_times):
            line_color = 'red' if idx == max_contrast_index else 'gray'
            axs[0].axvline(mid_time, color=line_color, linestyle='--', linewidth=line_color == "red" and 2 or 0.5, alpha=line_color == "red" and 1 or 0.5, zorder=10)
            axs[1].axvline(mid_time, color=line_color, linestyle='--', linewidth=line_color == "red" and 2 or 0.5, alpha=line_color == "red" and 1 or 0.5, zorder=10)

        # Align the time index between the two plots
        min_time = self.section_features[0]["time"][0]
        max_time = self.section_features[-1]["time"][1]
        axs[0].set_xlim(min_time, max_time)
        axs[1].set_xlim(min_time, max_time)
        # This code add some padding to the contrast plot make it look better
        axs[1].set_ylim(min(self.sections_contrasts)-20, max(self.sections_contrasts)+20)

        # Apply the formatter to the x-axis of both subplots
        axs[0].xaxis.set_major_formatter(FuncFormatter(format_func))
        axs[1].xaxis.set_major_formatter(FuncFormatter(format_func))

        plt.tight_layout()
        plt.show()

    def getHighestContrastSectionTime(self):
        # get most contribute
        start_1 = seconds_to_mm_ss(self.section_features[self.max_section]["time"][0])
        end_1 = seconds_to_mm_ss(self.section_features[self.max_section]["time"][1])

        start_2 = seconds_to_mm_ss(self.section_features[self.max_section+1]["time"][0])
        end_2 = seconds_to_mm_ss(self.section_features[self.max_section+1]["time"][1])
        return start_1, end_1,start_2,end_2