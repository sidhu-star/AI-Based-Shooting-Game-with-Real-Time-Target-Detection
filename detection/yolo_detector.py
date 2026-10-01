from pathlib import Path
from ultralytics import YOLO
from config import YOLO_MODEL, CONFIDENCE_THRESHOLD

class YOLODetector:
    def __init__(self):
        self.model_path = Path(YOLO_MODEL)
        self.model = YOLO(str(self.model_path) if self.model_path.exists() else "yolo11n.pt")

    def detect(self, frame):
        if frame is None:
            return []
        results = self.model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
        detections = []
        if not results:
            return detections
        result = results[0]
        names = result.names
        boxes = result.boxes
        if boxes is None:
            return detections
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            detections.append({
                "class_id": cls_id,
                "label": names.get(cls_id, str(cls_id)),
                "confidence": conf,
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "cx": (x1 + x2) // 2,
                "cy": (y1 + y2) // 2
            })
        return detections
