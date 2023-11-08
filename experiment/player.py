import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.transforms as mtransforms
import matplotlib.animation as animation
import pygame

class SafeFuncAnimation(animation.FuncAnimation):
    def _stop(self, *args):
        self.event_source.stop()
        try:
            self._fig.canvas.mpl_disconnect(self._resize_id)
        except AttributeError:
            pass
class Player:
    def __init__(self, song):
        self.song = song
        self.section_features = song.section_features
        self.title = song.title
        self.artist = song.artist
        self.inspect_feature = song.inspect_feature
        self.sections_contrasts = song.sections_contrasts
        self.file = song.file
        self.line = None
        self.line_1 = None
        self.clicked_time = 0

        pygame.init()
        pygame.mixer.init()

    def format_func(self, value, tick_number):
        minutes = int(value // 60)
        seconds = int(value % 60)
        return "{:02d}:{:02d}".format(minutes, seconds)

    def update_player_indicator(self, frame):
        current_time = (pygame.mixer.music.get_pos() / 1000.0) + self.clicked_time
        print(current_time)
        if self.line is None:
            self.line = self.axs[0].axvline(current_time, color='blue', linestyle='-', alpha=0.8)
            self.line_1 = self.axs[1].axvline(current_time, color='blue', linestyle='-', alpha=0.8)
        else:
            self.line.set_xdata(current_time)
            self.line_1.set_xdata(current_time)
        return self.line, self.line_1

    def play_audio(self, start_time):
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(start_time)

    def onclick(self, event):
        if event.inaxes == self.axs[0]:
            time_clicked = event.xdata
            for idx, section in enumerate(self.section_features):
                if section["time"][0] <= time_clicked <= section["time"][1]:
                    self.play_audio(section["time"][0])
                    if self.line is None:
                        self.line = self.axs[0].axvline(section["time"][0], color='blue', linestyle='-', alpha=0.8)
                        self.line_1 = self.axs[1].axvline(section["time"][0], color='blue', linestyle='-', alpha=0.8)
                    else:
                        self.line.set_xdata(section["time"][0])
                        self.line_1.set_xdata(section["time"][0])
                    self.clicked_time = section["time"][0]
                    plt.draw()
                    break

    def show(self):
        fig, axs = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios': [3, 1]})

        # Get unique labels and assign a color to each
        unique_labels = list(set(section["label"] for section in self.section_features))

        if len(unique_labels) > 20:
            print("Warning: There are more than 20 unique labels, colors may repeat.")

        colors = plt.cm.tab20(np.linspace(0, 1, 20))
        color_mapping = {label: colors[idx % 20] for idx, label in enumerate(unique_labels)}

        # Top plot
        for idx, section in enumerate(self.section_features):
            if len(section["feature"].shape) > 1:
                section["feature"] = np.mean(section["feature"], axis=-1)
            times = np.linspace(section["time"][0], section["time"][1], len(section["feature"]))
            start_time_str = self.format_func(section["time"][0], None)
            end_time_str = self.format_func(section["time"][1], None)

            # Use the color mapping based on the section's label
            color = color_mapping[section["label"]]

            axs[0].plot(times, section["feature"], color=color,
                        label=f"Section: {start_time_str} to {end_time_str} ({section['label']})", alpha=0.8)

        axs[0].set_title('{} - {}\n{} over Time'.format(self.title, self.artist, self.inspect_feature))
        axs[0].set_xlabel('Time (mm:ss)')
        axs[0].set_ylabel(self.inspect_feature)
        axs[0].grid(True)

        # Bottom plot
        max_contrast_index = np.argmax(self.sections_contrasts)
        mid_times = [(section["time"][1] + self.section_features[idx + 1]["time"][0]) / 2 for idx, section in
                     enumerate(self.section_features[:-1])]

        axs[1].plot(mid_times, self.sections_contrasts, color='black', zorder=1, label="Contrast Values",
                    linewidth=1.5, alpha=0.8)
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

        for idx, mid_time in enumerate(mid_times):
            line_color = 'red' if idx == max_contrast_index else 'gray'
            axs[0].axvline(mid_time, color=line_color, linestyle='--', linewidth=line_color == "red" and 2 or 0.5,
                           alpha=line_color == "red" and 1 or 0.5, zorder=10)
            axs[1].axvline(mid_time, color=line_color, linestyle='--', linewidth=line_color == "red" and 2 or 0.5,
                           alpha=line_color == "red" and 1 or 0.5, zorder=10)

        # Align the time index between the two plots
        min_time = self.section_features[0]["time"][0]
        max_time = self.section_features[-1]["time"][1]
        axs[0].set_xlim(min_time, max_time)
        axs[1].set_xlim(min_time, max_time)
        axs[1].set_ylim(min(self.sections_contrasts) - 20, max(self.sections_contrasts) + 20)

        axs[0].xaxis.set_major_formatter(FuncFormatter(self.format_func))
        axs[1].xaxis.set_major_formatter(FuncFormatter(self.format_func))

        plt.tight_layout()

        # Connect the button press event to the onclick function
        self.fig = fig
        self.axs = axs
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # Create an animation to update the player indicator
        self.ani = SafeFuncAnimation(self.fig, self.update_player_indicator, blit=True, interval=100)

        plt.show()

# You can then instantiate the Player class with your song data and use it as before.
