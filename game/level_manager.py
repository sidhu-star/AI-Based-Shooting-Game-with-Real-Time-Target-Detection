from config import LEVEL_TARGETS

class LevelManager:
    def __init__(self):
        self.level = 1

    def settings(self):
        return LEVEL_TARGETS[self.level]

    def advance(self):
        if self.level < max(LEVEL_TARGETS):
            self.level += 1
            return True
        return False

    def reset(self):
        self.level = 1
