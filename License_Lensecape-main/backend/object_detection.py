from ultralytics import YOLO
import supervision as sv

def initialize_yolo_model(model_path):
    return YOLO(model_path)

def perform_object_detection(model, frame):
    return model(frame)[0]

def annotate_frame(frame, detections, labels):
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    return box_annotator.annotate(scene=frame, detections=detections, labels=labels)
