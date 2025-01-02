# import cv2
# import time
# import numpy as np
# from sort import Sort  # Assuming you have SORT algorithm implemented in `sort.py`
# import mediapipe as mp
# from ultralytics import YOLO  # Importing YOLOv5 from the `ultralytics` library

# # Load YOLO model
# model = YOLO("yolo11s.pt")  # Replace with your custom-trained model file if needed

# # Mediapipe Pose model
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()

# # Initialize SORT Tracker
# tracker = Sort()

# # Timers for tracked objects
# timers = {}

# person_paths = {}  # Dictionary to store the movement path of each person

# # Sitting/standing threshold
# SITTING_THRESHOLD = 0.1  # Adjust based on experiments

# # Start video capture
# cap = cv2.VideoCapture(0)  # Replace 0 with the path to a video file if needed

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     height, width, _ = frame.shape

#     # Perform YOLO detection
#     results = model(frame)
#     detections = []
#     for result in results[0].boxes:
#         x1, y1, x2, y2 = map(int, result.xyxy[0])
#         confidence = result.conf.item()
#         class_id = int(result.cls.item())
#         if class_id == 0 and confidence > 0.5:  # Only process 'person' class
#             detections.append([x1, y1, x2, y2, confidence, class_id])  # Include class ID


#     detections = np.array(detections)

#     # Update SORT tracker
#     tracked_objects = tracker.update(detections)

#     # Inside the loop that processes tracked objects
#     for obj in tracked_objects:
#         # Inspect the returned object for debugging
#         print("Tracked Object:", obj)

#         # Unpack bounding box coordinates and object ID
#         x1, y1, x2, y2, obj_id = map(int, obj[:5])  # Take only the required 5 values

#         # Crop the detected person for pose estimation
#         person_crop = frame[y1:y2, x1:x2]
#         if person_crop.size > 0:
#             person_rgb = cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB)
#             results = pose.process(person_rgb)

#            # Analyze pose to determine sitting/standing or no position
#             if results.pose_landmarks:
#                 landmarks = results.pose_landmarks.landmark
#                 hip_y = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y +
#                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y) / 2
#                 knee_y = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y +
#                         landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y) / 2

#                 # Conditions for Sitting and Standing
#                 if (hip_y - knee_y) < SITTING_THRESHOLD:
#                     position = "Sitting"
#                 elif (hip_y - knee_y) >= SITTING_THRESHOLD:
#                     position = "Standing"
#                 else:
#                     position = "No Position"

#                 # Update centroids and draw movement path
#                 centroid = ((x1 + x2) // 2, (y1 + y2) // 2)

#                 # Initialize or update path for the person
#                 if obj_id not in person_paths:
#                     person_paths[obj_id] = []
#                 person_paths[obj_id].append(centroid)

#                 # Limit the length of the path
#                 MAX_PATH_LENGTH = 50
#                 if len(person_paths[obj_id]) > MAX_PATH_LENGTH:
#                     person_paths[obj_id].pop(0)

#                 # Draw path lines
#                 for i in range(1, len(person_paths[obj_id])):
#                     if person_paths[obj_id][i - 1] is None or person_paths[obj_id][i] is None:
#                         continue
#                     cv2.line(frame, person_paths[obj_id][i - 1], person_paths[obj_id][i], (0, 255, 255), 2)


#                 # Initialize timers for the object if not already present
#                 if obj_id not in timers:
#                     timers[obj_id] = {"start_time": time.time(), "position": position, "sitting_time": 0, "standing_time": 0}

#                 # Update timers if position changes
#                 current_time = time.time()
#                 if timers[obj_id]["position"] != position:
#                     elapsed = current_time - timers[obj_id]["start_time"]
#                     timers[obj_id][f"{timers[obj_id]['position'].lower()}_time"] += elapsed
#                     timers[obj_id]["start_time"] = current_time
#                     timers[obj_id]["position"] = position

#                 # Calculate elapsed time
#                 elapsed_time = current_time - timers[obj_id]["start_time"]

#                 # Draw bounding box and label
#                 color = (255, 0, 0) if position == "Sitting" else (0, 255, 0)
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#                 cv2.putText(frame, f"ID: {obj_id}, {position}", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#                 # Display the timer information
#                 sitting_time = timers[obj_id]["sitting_time"] if position == "Standing" else elapsed_time
#                 standing_time = timers[obj_id]["standing_time"] if position == "Sitting" else elapsed_time
#                 cv2.putText(frame, f"S: {sitting_time:.1f}s | St: {standing_time:.1f}s", (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)



#     # Display frame
#     cv2.imshow("Classroom Activity Tracker", frame)

#     # Quit on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# # Print final sitting/standing durations
# for obj_id, times in timers.items():
#     print(f"Person {obj_id}:")
#     print(f"  Sitting Time: {times['sitting_time']:.2f} seconds")
#     print(f"  Standing Time: {times['standing_time']:.2f} seconds")


import cv2
import time
import numpy as np
from sort import Sort  # Assuming you have SORT algorithm implemented in `sort.py`
import mediapipe as mp
from ultralytics import YOLO  # Importing YOLOv5 from the `ultralytics` library

# Load YOLO model
model = YOLO("yolo11s.pt")  # Replace with your custom-trained model file if needed

# Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize SORT Tracker
tracker = Sort()

# Timers for tracked objects
timers = {}

person_paths = {}  # Dictionary to store the movement path of each person

# Function to detect sitting or standing
def detect_sitting_or_standing(results):
    if not results.pose_landmarks:
        return "No pose detected"

    # Extract landmark positions
    landmarks = results.pose_landmarks.landmark

    # Get key landmark coordinates
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    # Calculate vertical distances
    hip_to_knee_avg = (left_hip.y - left_knee.y + right_hip.y - right_knee.y) / 2
    shoulder_to_hip_avg = (left_shoulder.y - left_hip.y + right_shoulder.y - right_hip.y) / 2

    # Define thresholds
    SITTING_THRESHOLD = 0.2  # Distance between hips and knees for sitting
    STANDING_THRESHOLD = 0.3  # Distance between shoulders and hips for standing

    # Detect sitting: Hips are closer to knees
    if hip_to_knee_avg < SITTING_THRESHOLD and shoulder_to_hip_avg > STANDING_THRESHOLD:
        return "Sitting"

    # Detect standing: Hips are further from knees and shoulders are aligned
    if hip_to_knee_avg > SITTING_THRESHOLD and shoulder_to_hip_avg > STANDING_THRESHOLD:
        return "Standing"

    # If neither condition is met
    return "Idle"

# Sitting/standing threshold
SITTING_THRESHOLD = 0.5  # Adjust based on experiments
MIN_HEIGHT_THRESHOLD = 150  # Minimum height of the bounding box for full-body detection

# Start video capture
cap = cv2.VideoCapture(0)  # Replace 0 with the path to a video file if needed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # Perform YOLO detection
    results = model(frame)
    detections = []
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        confidence = result.conf.item()
        class_id = int(result.cls.item())
        box_height = y2 - y1
        if class_id == 0 and confidence > 0.5 and box_height > MIN_HEIGHT_THRESHOLD:  # Only process full-body detections
            detections.append([x1, y1, x2, y2, confidence, class_id])  # Include class ID

    detections = np.array(detections)
    if len(detections) == 0:
        detections = np.empty((0, 6))  # Ensure it matches the expected format with 6 columns

    # Update SORT tracker
    tracked_objects = tracker.update(detections)

    # Inside the loop that processes tracked objects
    for obj in tracked_objects:
        # Unpack bounding box coordinates and object ID
        x1, y1, x2, y2, obj_id = map(int, obj[:5])  # Take only the required 5 values

        # Crop the detected person for pose estimation
        person_crop = frame[y1:y2, x1:x2]
        if person_crop.size > 0:
            person_rgb = cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB)
            results = pose.process(person_rgb)

            position = detect_sitting_or_standing(results)

                # Update centroids and draw movement path
            centroid = ((x1 + x2) // 2, (y1 + y2) // 2)

            if obj_id not in person_paths:
                person_paths[obj_id] = []
            person_paths[obj_id].append(centroid)

            MAX_PATH_LENGTH = 50
            if len(person_paths[obj_id]) > MAX_PATH_LENGTH:
                person_paths[obj_id].pop(0)

            for i in range(1, len(person_paths[obj_id])):
                if person_paths[obj_id][i - 1] is None or person_paths[obj_id][i] is None:
                    continue
                cv2.line(frame, person_paths[obj_id][i - 1], person_paths[obj_id][i], (0, 255, 255), 2)

            # Initialize timers for the object if not already present
            # Initialize timers for the object if not already present
            if obj_id not in timers:
                timers[obj_id] = {
                    "start_time": time.time(),
                    "position": position,
                    "sitting_time": 0,
                    "standing_time": 0,
                    "idle_time": 0  # Initialize idle time
                }

            # Update timers if position changes
            current_time = time.time()
            if timers[obj_id]["position"] != position:
                elapsed = current_time - timers[obj_id]["start_time"]
                if timers[obj_id]["position"].lower() in ["sitting", "standing", "idle"]:
                    timers[obj_id][f"{timers[obj_id]['position'].lower()}_time"] += elapsed
                timers[obj_id]["start_time"] = current_time
                timers[obj_id]["position"] = position

            # Calculate elapsed time
            elapsed_time = current_time - timers[obj_id]["start_time"]

            # Draw bounding box and styled overlay
            overlay_color = (255, 255, 0) if position == "Idle" else (255, 0, 0 if position == "Sitting" else 0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), overlay_color, 2)

            # Add semi-transparent overlay for ID and timer
            overlay = frame.copy()
            alpha = 0.6
            cv2.rectangle(overlay, (x1, y1 - 60), (x2, y1), overlay_color, -1)
            frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

            # Display ID, position, and timing in a styled way
            cv2.putText(frame, f"ID: {obj_id}", (x1 + 5, y1 - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Pos: {position}", (x1 + 5, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"S: {timers[obj_id]['sitting_time']:.1f}s | St: {timers[obj_id]['standing_time']:.1f}s | I: {timers[obj_id]['idle_time']:.1f}s",
                        (x1 + 5, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


    # Display frame
    cv2.imshow("Enhanced Classroom Activity Tracker", frame)

    # Quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print final sitting/standing durations
for obj_id, times in timers.items():
    print(f"Person {obj_id}:")
    print(f"  Sitting Time: {times['sitting_time']:.2f} seconds")
    print(f"  Standing Time: {times['standing_time']:.2f} seconds")


