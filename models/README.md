# Custom YOLO model

The repository supports a custom target class.

Train with:

python scripts/generate_dataset.py
python train.py

After training, copy runs/target_detector/weights/best.pt to models/target.pt and set YOLO_MODEL = 'models/target.pt' in config.py.

The generated dataset is synthetic and intended to verify the training pipeline. For a stronger detector, collect varied real webcam images and annotate them with YOLO labels.
