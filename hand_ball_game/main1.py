import cv2
import numpy as np

# Initialize variables
ball_pos = [320, 240]  # Center
ball_dir = [4, 2]      # Movement
left_rod, right_rod = 200, 200  # Rod positions

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    height, width = frame.shape[:2]

    # Draw Ball
    cv2.circle(frame, tuple(ball_pos), 10, (0, 0, 255), -1)

    # Draw Rods
    cv2.rectangle(frame, (20, left_rod), (40, left_rod + 100), (255, 0, 0), -1)
    cv2.rectangle(frame, (width-40, right_rod), (width-20, right_rod + 100), (0, 255, 0), -1)

    # Ball Movement
    ball_pos[0] += ball_dir[0]
    ball_pos[1] += ball_dir[1]

    # Collision with walls
    if ball_pos[1] <= 0 or ball_pos[1] >= height:
        ball_dir[1] = -ball_dir[1]

    # Collision with rods
    if 20 < ball_pos[0] < 40 and left_rod < ball_pos[1] < left_rod + 100:
        ball_dir[0] = -ball_dir[0]
    elif width-40 < ball_pos[0] < width-20 and right_rod < ball_pos[1] < right_rod + 100:
        ball_dir[0] = -ball_dir[0]

    # Loss condition
    if ball_pos[0] <= 0 or ball_pos[0] >= width:
        winner = "Right" if ball_pos[0] <= 0 else "Left"
        print(f"{winner} Wins!")
        break

    cv2.imshow("Game", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
