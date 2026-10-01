class ScoreManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.best_combo = 0

    def hit(self, points):
        self.hits += 1
        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        multiplier = 1 + min(self.combo // 5, 4) * 0.25
        earned = int(points * multiplier)
        self.score += earned
        return earned

    def miss(self):
        self.misses += 1
        self.combo = 0

    @property
    def accuracy(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total else 0.0
