import random

class TargetManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.radius = 50
        self.reset()

    def reset(self):
        self.x = self.width // 2
        self.y = self.height // 2
        self.active = True

    def configure(self, radius):
        self.radius = radius
        self.move()

    def move(self):
        margin = self.radius + 30
        self.x = random.randint(margin, self.width - margin)
        self.y = random.randint(120 + self.radius, self.height - self.radius - 20)

    def hit(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2
