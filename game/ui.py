import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.title = pygame.font.SysFont("Segoe UI", 30, bold=True)
        self.big = pygame.font.SysFont("Segoe UI", 48, bold=True)
        self.medium = pygame.font.SysFont("Segoe UI", 22, bold=True)
        self.small = pygame.font.SysFont("Segoe UI", 17)

    def text(self, value, font, x, y, color=(235,238,245)):
        self.screen.blit(font.render(str(value), True, color), (x, y))

    def panel(self, rect, fill=(25,29,40), border=(65,72,90)):
        pygame.draw.rect(self.screen, fill, rect, border_radius=16)
        pygame.draw.rect(self.screen, border, rect, 1, border_radius=16)

    def header(self, score, level, time_left):
        pygame.draw.rect(self.screen, (17,20,28), (0,0,1200,82))
        self.text("TARGET ARENA", self.title, 28, 24)
        self.text(f"LEVEL {level}", self.medium, 430, 28, (110,210,255))
        self.text(f"SCORE {score}", self.medium, 600, 28, (255,210,90))
        self.text(f"TIME {max(0,int(time_left)):02d}", self.medium, 850, 28, (120,235,160))

    def sidebar(self, hits, misses, accuracy, combo, detections, fps):
        self.panel((930,105,245,600))
        self.text("LIVE STATUS", self.medium, 955, 130)
        values = [
            ("HITS", hits), ("MISSES", misses), ("ACCURACY", f"{accuracy:.1f}%"),
            ("COMBO", f"x{combo}"), ("YOLO TARGETS", detections), ("FPS", int(fps))
        ]
        y = 185
        for label, value in values:
            self.text(label, self.small, 955, y, (155,165,185))
            self.text(value, self.medium, 955, y+25)
            y += 78

    def crosshair(self, x, y):
        pygame.draw.circle(self.screen, (255,255,255), (x,y), 18, 2)
        pygame.draw.line(self.screen, (255,255,255), (x-28,y), (x+28,y), 2)
        pygame.draw.line(self.screen, (255,255,255), (x,y-28), (x,y+28), 2)

    def centered(self, value, y):
        s = self.big.render(value, True, (245,245,250))
        self.screen.blit(s, s.get_rect(center=(600,y)))
