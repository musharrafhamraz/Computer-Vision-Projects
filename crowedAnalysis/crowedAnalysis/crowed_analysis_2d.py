from ultralytics import YOLO
import cv2
import numpy as np

# Load a pre-trained YOLOv8 model
model = YOLO('crowedAnalysis/yolov8n.pt')  # Use 'yolov8x.pt' for higher accuracy

video_path = r'C:\\Users\\PMLS\\Desktop\\Local Disk\\CV\\computer vision adv\\crowedAnalysis\\people.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

# Define grid size for heatmap
grid_size = 10
ret, first_frame = cap.read()
if not ret:
    print("Failed to read the first frame")
    exit()

height, width, _ = first_frame.shape
cell_height, cell_width = height // grid_size, width // grid_size

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame)

    # Filter detections for 'person' class
    detections = results[0].boxes  # YOLO's detected objects
    person_detections = [box for box in detections if box.cls == 0]  # '0' is typically the 'person' class

    # Draw bounding boxes
    for box in person_detections:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display count
    cv2.putText(frame, f"Count: {len(person_detections)}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Generate density map
    density_map = np.zeros((grid_size, grid_size), dtype=int)
    for box in person_detections:
        x_center = (box.xyxy[0, 0] + box.xyxy[0, 2]) // 2
        y_center = (box.xyxy[0, 1] + box.xyxy[0, 3]) // 2
        cell_x = int(x_center // cell_width)
        cell_y = int(y_center // cell_height)
        if 0 <= cell_x < grid_size and 0 <= cell_y < grid_size:
            density_map[cell_y, cell_x] += 1

    # Create a color-coded heatmap
    heatmap = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(grid_size):
        for j in range(grid_size):
            density = density_map[i, j]
            if density > 5:  # High density
                color = (0, 0, 255)  # Red
            elif density > 2:  # Medium density
                color = (0, 255, 0)  # Green
            elif density > 0:  # Low density
                color = (255, 0, 0)  # Blue
            else:  # No density
                color = (0, 0, 0)  # Black

            # Draw patches for the grid cell
            x1, y1 = j * cell_width, i * cell_height
            x2, y2 = x1 + cell_width, y1 + cell_height
            cv2.rectangle(heatmap, (x1, y1), (x2, y2), color, -1)

    # Resize frames to equal widths for display
    resized_frame = cv2.resize(frame, (width // 2, height))
    resized_heatmap = cv2.resize(heatmap, (width // 2, height))

    # Concatenate video and heatmap
    combined_frame = cv2.hconcat([resized_frame, resized_heatmap])

    # Display combined frame
    cv2.imshow('Crowd Analysis & Heatmap', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()