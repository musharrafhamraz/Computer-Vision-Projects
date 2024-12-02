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

# Define grid size for the heatmap
grid_size = 10
ret, first_frame = cap.read()
if not ret:
    print("Failed to read the first frame")
    exit()

height, width, _ = first_frame.shape
cell_height, cell_width = height // grid_size, width // grid_size

# Define high-density threshold
density_threshold = 3

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame)

    # Filter detections for 'person' class
    detections = results[0].boxes
    person_detections = [box for box in detections if box.cls == 0]

    # Draw bounding boxes on the frame
    for box in person_detections:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'Person {confidence:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Generate density map
    density_map = np.zeros((grid_size, grid_size), dtype=int)
    for box in person_detections:
        x_center = (box.xyxy[0, 0] + box.xyxy[0, 2]) // 2
        y_center = (box.xyxy[0, 1] + box.xyxy[0, 3]) // 2
        cell_x = int(x_center // cell_width)
        cell_y = int(y_center // cell_height)
        if 0 <= cell_x < grid_size and 0 <= cell_y < grid_size:
            density_map[cell_y, cell_x] += 1

    # Overlay high-density areas on the video frame
    for row in range(grid_size):
        for col in range(grid_size):
            density = density_map[row, col]
            if density >= density_threshold:
                # Calculate cell coordinates
                start_x = col * cell_width
                start_y = row * cell_height
                end_x = start_x + cell_width
                end_y = start_y + cell_height

                # Overlay a red transparent patch for high-density cells
                overlay_color = (0, 0, 255)  # Red in BGR
                alpha = 0.5  # Transparency level
                sub_frame = frame[start_y:end_y, start_x:end_x]
                overlay = np.full(sub_frame.shape, overlay_color, dtype=np.uint8)
                cv2.addWeighted(overlay, alpha, sub_frame, 1 - alpha, 0, sub_frame)

    # Display the video frame with overlays
    cv2.imshow('Crowd Analysis with High-Density Segmentation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
