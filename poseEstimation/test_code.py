# import cv2
# import mediapipe as mp
# import time

# # Initialize MediaPipe Pose
# mpPose = mp.solutions.pose
# pose = mpPose.Pose()
# mpDraw = mp.solutions.drawing_utils

# # Start video capture
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280) 
# cap.set(4, 720)
# pTime = 0

# # Function to detect running or jumping
# def detect_pose(results):
#     if not results.pose_landmarks:
#         return "No pose detected"
    
#     # Extract landmark positions
#     landmarks = results.pose_landmarks.landmark
    
#     # Get key landmark coordinates
#     left_knee = landmarks[mpPose.PoseLandmark.LEFT_KNEE]
#     right_knee = landmarks[mpPose.PoseLandmark.RIGHT_KNEE]
#     left_hip = landmarks[mpPose.PoseLandmark.LEFT_HIP]
#     right_hip = landmarks[mpPose.PoseLandmark.RIGHT_HIP]
#     left_shoulder = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER]
#     right_shoulder = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER]

#     # Calculate distances
#     hip_to_knee_avg = (left_hip.y - left_knee.y + right_hip.y - right_knee.y) / 2
#     shoulder_movement = abs(left_shoulder.y - right_shoulder.y)

#     # Running detection: Rapid shoulder movement with small knee-to-hip distance
#     if shoulder_movement > 0.05 and hip_to_knee_avg < 0.3:
#         return "Running"

#     # Jumping detection: Both knees are significantly higher than hips
#     # if left_knee.y < left_hip.y and right_knee.y < right_hip.y:
#     if left_knee.y < left_hip.y:
#         return "Jumping"
    
#     return "Standing or idle"

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     # Convert the image to RGB for MediaPipe processing
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = pose.process(imgRGB)

#     # Draw pose landmarks on the image
#     if results.pose_landmarks:
#         mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

#     # Detect pose and display it
#     pose_status = detect_pose(results)
#     cv2.putText(img, pose_status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     # Display FPS
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f"FPS: {int(fps)}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#     # Show the image
#     cv2.imshow('Pose Detection', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import pygame
import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pose Detection Game")

# Circle properties
circle_radius = 20
circle_x = 100
circle_y = screen_height - 50
circle_velocity = 5  # Speed at which the circle moves

# Platform properties
platform_width = 200
platform_height = 20
platform_x = 300
platform_y = screen_height - 50

# Initialize video capture
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
    if left_knee.y < left_hip.y:
        return "Jumping"
    
    return "Idle"

# Main game loop
running = True
while running:
    success, img = cap.read()
    if not success:
        break

    # Convert the image to RGB for MediaPipe processing
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # Draw pose landmarks on the image
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    # Detect the pose and display it
    pose_status = detect_pose(results)
    
    # Check if the pose is running
    if pose_status == "Running":
        circle_x += circle_velocity  # Move the circle forward

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the platform
    pygame.draw.rect(screen, (0, 0, 0), (platform_x, platform_y, platform_width, platform_height))

    # Draw the circle
    pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), circle_radius)

    # Display the pose status
    font = pygame.font.SysFont('Arial', 30)
    text = font.render(f'Pose: {pose_status}', True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    fps_text = font.render(f'FPS: {int(fps)}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 50))

    # Update the display
    pygame.display.flip()

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Release resources
cap.release()
pygame.quit()
cv2.destroyAllWindows()