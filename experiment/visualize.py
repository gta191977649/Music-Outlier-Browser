import numpy as np
import librosa
import pygame


class AudioPlayer:
    def __init__(self, audio_file, width=800, height=400):
        self.audio_file = audio_file
        self.y, self.sr = librosa.load(audio_file, sr=None)

        # Compute the RMS energy
        self.rms = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=512)[0]
        self.frame_times = librosa.frames_to_time(np.arange(len(self.rms)), sr=self.sr, hop_length=512)

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('RMS Energy')
        self.clock = pygame.time.Clock()

        self.width = width
        self.height = height
        self.bar_width = width / len(self.rms)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse click to update playback position
                    x, y = event.pos
                    timestamp = x / self.width * self.frame_times[-1]
                    pygame.mixer.music.play(start=timestamp)

            self.draw()
            self.clock.tick(30)

        pygame.quit()

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Draw RMS energy bars
        scaling_factor = self.height - 50  # Reduce by 50 for some padding
        for i, r in enumerate(self.rms):
            bar_height = r * scaling_factor
            pygame.draw.rect(self.screen, (0, 0, 255),
                             (i * self.bar_width, self.height,
                              self.bar_width, -bar_height))

        # Draw position indicator
        if pygame.mixer.music.get_busy():
            pos_in_msec = pygame.mixer.music.get_pos()
            pos_in_sec = pos_in_msec / 1000.0
            x_pos = pos_in_sec / self.frame_times[-1] * self.width
            pygame.draw.line(self.screen, (255, 0, 0), (x_pos, 0), (x_pos, self.height), 2)

        pygame.display.flip()


audio_file = '../music/title.wav'
player = AudioPlayer(audio_file)
