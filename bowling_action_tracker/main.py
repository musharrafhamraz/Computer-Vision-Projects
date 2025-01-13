import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture('bowling.mp4')
# cap = cv2.resize((640, 480))
wrist_positions = []

# Function to convert normalized coordinates to pixel coordinates
def to_pixel_coords(landmark, frame):
    return int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1000, 600))
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extract right-hand keypoints
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        # Convert normalized coordinates to pixel coordinates
        shoulder_coords = to_pixel_coords(right_shoulder, frame)
        elbow_coords = to_pixel_coords(right_elbow, frame)
        wrist_coords = to_pixel_coords(right_wrist, frame)

        # Add wrist coordinates to the trajectory list
        wrist_positions.append(wrist_coords)

        # Draw right-hand keypoints
        cv2.circle(frame, shoulder_coords, 8, (0, 255, 0), -1)  # Shoulder
        cv2.circle(frame, elbow_coords, 8, (0, 255, 255), -1)   # Elbow
        cv2.circle(frame, wrist_coords, 8, (255, 0, 0), -1)     # Wrist

        # Draw line between elbow and wrist
        cv2.line(frame, elbow_coords, wrist_coords, (255, 0, 255), thickness=5)

        # Draw trajectory line for the wrist
        for i in range(1, len(wrist_positions)):
            cv2.line(frame, wrist_positions[i - 1], wrist_positions[i], (0, 0, 255), thickness=4)

    # Display the frame
    cv2.imshow('Bowler Wrist Tracking', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
