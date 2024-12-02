import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280) 
cap.set(4, 720)
pTime = 0

# Function to detect running or jumping
def detect_pose(results):
    if not results.pose_landmarks:
        return "No pose detected"
    
    # Extract landmark positions
    landmarks = results.pose_landmarks.landmark
    
    # Get key landmark coordinates
    left_knee = landmarks[mpPose.PoseLandmark.LEFT_KNEE]
    right_knee = landmarks[mpPose.PoseLandmark.RIGHT_KNEE]
    left_hip = landmarks[mpPose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks[mpPose.PoseLandmark.RIGHT_HIP]
    left_shoulder = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER]

    # Calculate distances
    hip_to_knee_avg = (left_hip.y - left_knee.y + right_hip.y - right_knee.y) / 2
    shoulder_movement = abs(left_shoulder.y - right_shoulder.y)

    # Running detection: Rapid shoulder movement with small knee-to-hip distance
    if shoulder_movement > 0.05 and hip_to_knee_avg < 0.3:
        return "Running"

    # Jumping detection: Both knees are significantly higher than hips
    # if left_knee.y < left_hip.y and right_knee.y < right_hip.y:
    if left_knee.y < left_hip.y:
        return "Jumping"
    
    return "Standing or idle"

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert the image to RGB for MediaPipe processing
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # Draw pose landmarks on the image
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    # Detect pose and display it
    pose_status = detect_pose(results)
    cv2.putText(img, pose_status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show the image
    cv2.imshow('Pose Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
