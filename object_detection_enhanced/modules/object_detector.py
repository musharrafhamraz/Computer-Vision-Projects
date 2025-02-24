from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):  # Pre-trained YOLOv8 nano model
        self.model = YOLO(model_path)

    def detect_objects(self, frame, hand_pos=None):
        results = self.model(frame)
        detected_objects = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = self.model.names[int(box.cls)]
                confidence = float(box.conf)
                
                if hand_pos and self._is_near_hand(hand_pos, (x1, y1, x2, y2)):
                    detected_objects.append({
                        "label": label,
                        "confidence": confidence,
                        "box": (x1, y1, x2, y2)
                    })
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return detected_objects

    def _is_near_hand(self, hand_pos, box):
        hx, hy = hand_pos
        x1, y1, x2, y2 = box
        return x1 <= hx <= x2 and y1 <= hy <= y2