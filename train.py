from ultralytics import YOLO
from pathlib import Path

DATA = Path('dataset/data.yaml')
MODEL = 'yolo11n.pt'

if __name__ == '__main__':
    if not DATA.exists():
        raise FileNotFoundError('dataset/data.yaml not found. Run scripts/generate_dataset.py first.')
    model = YOLO(MODEL)
    model.train(data=str(DATA), epochs=40, imgsz=640, batch=8, project='runs', name='target_detector')
    print('Training complete. Copy runs/target_detector/weights/best.pt to models/target.pt')
