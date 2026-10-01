import math
import pygame
import numpy as np

class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False

    def _tone(self, frequency, duration_ms, volume=0.18):
        if not self.enabled:
            return
        sample_rate = 44100
        count = int(sample_rate * duration_ms / 1000)
        wave = np.sin(2 * math.pi * frequency * np.arange(count) / sample_rate)
        audio = (wave * 32767 * volume).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        pygame.sndarray.make_sound(stereo).play()

    def hit(self):
        self._tone(880, 90)

    def miss(self):
        self._tone(220, 120)

    def level_up(self):
        self._tone(660, 100)
        pygame.time.delay(40)
        self._tone(990, 140)

    def game_over(self):
        self._tone(440, 120)
        pygame.time.delay(50)
        self._tone(220, 220)

    def close(self):
        if self.enabled:
            pygame.mixer.quit()
