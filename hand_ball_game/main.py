import cv2
import numpy as np
import mediapipe as mp
import random

# Initialize Mediapipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Game settings
window_width, window_height = 800, 600
ball_radius = 20
ball_speed = [8, 8]  # [x_speed, y_speed]
ball_position = [window_width // 2, window_height // 2]

# Rod settings
rod_height = 150
rod_width = 20
left_rod_x = 50
right_rod_x = window_width - 50

# Score
score = [0, 0]  # [left_player, right_player]

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

def detect_hand_landmarks(image, results):
    hand_positions = {"left": None, "right": None}
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_class in zip(results.multi_hand_landmarks, results.multi_handedness):
            x_coords = [lm.x for lm in hand_landmarks.landmark]
            y_coords = [lm.y for lm in hand_landmarks.landmark]
            hand_center = (int(np.mean(x_coords) * window_width), int(np.mean(y_coords) * window_height))
            
            if hand_class.classification[0].label == "Left":
                hand_positions["left"] = hand_center
            else:
                hand_positions["right"] = hand_center
    return hand_positions

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and resize the frame
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (window_width, window_height))

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Detect hand positions
    hand_positions = detect_hand_landmarks(rgb_frame, results)

    # Update rods' positions based on hand detection
    if hand_positions["left"]:
        left_rod_y = hand_positions["left"][1] - rod_height // 2
    else:
        left_rod_y = window_height // 2 - rod_height // 2

    if hand_positions["right"]:
        right_rod_y = hand_positions["right"][1] - rod_height // 2
    else:
        right_rod_y = window_height // 2 - rod_height // 2

    # Ball movement
    ball_position[0] += ball_speed[0]
    ball_position[1] += ball_speed[1]

    # Ball collision with top and bottom
    if ball_position[1] <= ball_radius or ball_position[1] >= window_height - ball_radius:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with left rod
    if (
        ball_position[0] - ball_radius <= left_rod_x + rod_width
        and left_rod_y <= ball_position[1] <= left_rod_y + rod_height
    ):
        ball_speed[0] = -ball_speed[0]
    elif ball_position[0] - ball_radius <= 0:
        score[1] += 1
        ball_position = [window_width // 2, window_height // 2]

    # Ball collision with right rod
    if (
        ball_position[0] + ball_radius >= right_rod_x - rod_width
        and right_rod_y <= ball_position[1] <= right_rod_y + rod_height
    ):
        ball_speed[0] = -ball_speed[0]
    elif ball_position[0] + ball_radius >= window_width:
        score[0] += 1
        ball_position = [window_width // 2, window_height // 2]

    # Draw elements on the frame
    cv2.circle(frame, tuple(ball_position), ball_radius, (0, 255, 0), -1)  # Ball
    cv2.rectangle(frame, (left_rod_x, left_rod_y), (left_rod_x + rod_width, left_rod_y + rod_height), (255, 0, 0), -1)  # Left rod
    cv2.rectangle(frame, (right_rod_x - rod_width, right_rod_y), (right_rod_x, right_rod_y + rod_height), (0, 0, 255), -1)  # Right rod
    cv2.putText(frame, f"Left Player: {score[0]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Right Player: {score[1]}", (window_width - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("Hand-Controlled Game", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
