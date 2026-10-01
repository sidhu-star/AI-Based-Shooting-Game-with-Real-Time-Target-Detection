import time
import cv2
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_DURATION, LEVEL_TARGETS, LEADERBOARD_FILE
from detection.camera import Camera
from detection.yolo_detector import YOLODetector
from game.target_manager import TargetManager
from game.level_manager import LevelManager
from game.score_manager import ScoreManager
from game.ui import UI
from audio.sound_manager import SoundManager
from leaderboard.leaderboard import Leaderboard

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Target Arena - Real-Time YOLO Detection")
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.detector = YOLODetector()
        self.target = TargetManager(900, SCREEN_HEIGHT)
        self.levels = LevelManager()
        self.score = ScoreManager()
        self.ui = UI(self.screen)
        self.sound = SoundManager()
        self.leaderboard = Leaderboard(LEADERBOARD_FILE)
        self.running = True
        self.started = False
        self.finished = False
        self.start_time = None
        self.flash = ""
        self.flash_until = 0
        self.last_detections = []
        self.current_frame = None
        self.fps = 0

    def start(self):
        self.score.reset()
        self.levels.reset()
        self.target.configure(LEVEL_TARGETS[1]["target_size"])
        self.start_time = time.time()
        self.started = True
        self.finished = False
        self.flash = ""

    def handle_hit(self, x, y):
        if self.target.hit(x, y):
            points = LEVEL_TARGETS[self.levels.level]["points"]
            earned = self.score.hit(points)
            self.flash = f"+{earned}"
            self.flash_until = time.time() + 0.5
            self.sound.hit()
            self.target.move()
            required = LEVEL_TARGETS[self.levels.level]["required_hits"]
            if self.score.hits >= required:
                if self.levels.advance():
                    self.target.configure(LEVEL_TARGETS[self.levels.level]["target_size"])
                    self.flash = f"LEVEL {self.levels.level}"
                    self.flash_until = time.time() + 1.2
                    self.sound.level_up()
                    self.score.hits = 0
                else:
                    self.finish()
        else:
            self.score.miss()
            self.flash = "MISS"
            self.flash_until = time.time() + 0.4
            self.sound.miss()

    def finish(self):
        if self.finished:
            return
        self.finished = True
        self.sound.game_over()
        self.leaderboard.add("Player", self.score.score, self.levels.level,
                             self.score.hits, self.score.misses, self.score.accuracy)

    def draw_camera_preview(self, frame):
        if frame is None:
            return
        preview = cv2.resize(frame, (900, 675))
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(preview.swapaxes(0,1))
        self.screen.blit(surface, (0,82))

    def draw(self):
        self.screen.fill((10,13,19))
        self.ui.header(self.score.score, self.levels.level, self.time_left())
        self.draw_camera_preview(self.current_frame)

        scale_x, scale_y = 900 / 640, 675 / 480
        for d in self.last_detections:
            x1 = int(d["x1"] * scale_x)
            y1 = int(d["y1"] * scale_y) + 82
            x2 = int(d["x2"] * scale_x)
            y2 = int(d["y2"] * scale_y) + 82
            pygame.draw.rect(self.screen, (80,230,140), (x1,y1,x2-x1,y2-y1), 2)

        mx, my = pygame.mouse.get_pos()
        self.ui.crosshair(mx, my)
        self.ui.sidebar(self.score.hits, self.score.misses, self.score.accuracy,
                        self.score.combo, len(self.last_detections), self.fps)

        if not self.started:
            self.ui.centered("PRESS ENTER TO START", 360)
        elif self.finished:
            self.ui.centered("GAME OVER", 350)
            self.ui.text("Press ENTER to play again", self.ui.medium, 455, 405)
        elif time.time() < self.flash_until:
            self.ui.centered(self.flash, 130)

        pygame.display.flip()

    def time_left(self):
        if not self.start_time or self.finished:
            return GAME_DURATION
        return GAME_DURATION - (time.time() - self.start_time)

    def run(self):
        self.start()
        previous = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_RETURN and (not self.started or self.finished):
                        self.start()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.started and not self.finished:
                        self.handle_hit(*pygame.mouse.get_pos())

            self.current_frame = self.camera.read()
            self.last_detections = self.detector.detect(self.current_frame)

            now = time.time()
            self.fps = 1 / max(now - previous, 1e-6)
            previous = now

            if self.started and not self.finished and self.time_left() <= 0:
                self.finish()

            self.draw()
            self.clock.tick(FPS)

    def shutdown(self):
        self.camera.release()
        self.sound.close()
        pygame.quit()
