SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 760
FPS = 60
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
YOLO_MODEL = "models/yolo11n.pt"
CONFIDENCE_THRESHOLD = 0.35
GAME_DURATION = 60
LEVEL_TARGETS = {
    1: {"duration": 60, "points": 10, "target_size": 55, "required_hits": 8},
    2: {"duration": 50, "points": 20, "target_size": 45, "required_hits": 10},
    3: {"duration": 40, "points": 30, "target_size": 38, "required_hits": 12},
    4: {"duration": 30, "points": 50, "target_size": 32, "required_hits": 15},
}
LEADERBOARD_FILE = "results/leaderboard.csv"
