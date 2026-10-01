# AI-Based Shooting Game with Real-Time Target Detection — Version 2

A safe virtual target game using a webcam, YOLO real-time detection, Pygame, sound effects, progressive levels, scoring, and a CSV leaderboard.

## Features

- Live webcam feed
- YOLO object detection overlays
- Detection labels and confidence
- Virtual on-screen targets and crosshair
- Four progressive levels
- Combo scoring and accuracy
- Runtime-generated sound effects
- Local leaderboard
- FPS and live detection statistics

This is a virtual computer game. It does not control, connect to, or simulate a real-world weapon or projectile.

## Install in VS Code

1. Clone this repository.
2. Open the folder in VS Code.
3. Run:

    python -m venv venv
    venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python main.py

The first YOLO run may download the pretrained yolo11n model.

## Controls

ENTER = start/restart
Mouse = move crosshair
Left mouse button = virtual target action
ESC = exit

## Architecture

Webcam -> OpenCV -> YOLO -> live detections -> Pygame UI -> virtual target interaction -> score/levels -> leaderboard

## Files

main.py is the entry point.
app.py contains the Version 2 game engine.
config.py contains game settings.
requirements.txt contains dependencies.
leaderboard.csv stores scores.

## Custom AI target model

For a true target-specific detector, train a custom YOLO model and set YOLO_MODEL in config.py to the resulting .pt file. Large model files are excluded by .gitignore.

## Testing

Install pytest if required:

    pip install pytest

Then run:

    pytest

## Future upgrades

- Custom target dataset
- Target-only YOLO class filtering
- Hand tracking for virtual aiming
- Difficulty selection
- Online leaderboard
- Analytics dashboard
