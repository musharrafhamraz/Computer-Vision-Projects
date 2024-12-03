import pygame
import cv2
import mediapipe as mp
import numpy as np
import time
import random

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

# Player properties (circle)
circle_radius = 20
circle_x = 100
circle_y = screen_height - 50
circle_velocity = 5  # Speed at which the player moves
circle_gravity = 0.8  # Gravity effect
circle_dy = 0  # Initial vertical speed
is_jumping = False
jump_duration = 0.1  # Time limit for a jump (seconds)
last_jump_time = 0  # Time of the last jump

# Platform properties
platform_width = 200
platform_height = 20
platform_y = screen_height - 50
platform_spawn_x = screen_width  # Spawn point for new platforms (off-screen)
platform_velocity = 2  # Speed at which platforms move
platforms = []  # List to store platform X positions

# Obstacles (optional)
obstacle_radius = 30
obstacle_y = screen_height - platform_height - 2 * obstacle_radius  # Y position below platform
obstacles = []  # List to store obstacle X positions (empty initially)
obstacle_shapes = ["rectangle", "triangle", "square"]
obstacle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
obstacle_speed = 6  # Increased speed

# Game settings and variables
game_speed = 1  # Overall game speed multiplier
score = 0
font = pygame.font.SysFont('Arial', 30)  # Font for text display
level = 1  # Game level
lives = 3  # Player lives

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

    # Jumping detection: Either knee significantly higher than the corresponding hip
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

    # Check if the pose is jumping
    if pose_status == "Jumping" and not is_jumping:
        is_jumping = True
        circle_dy = -15

    if is_jumping:
        circle_y += circle_dy
        circle_dy += circle_gravity
        if circle_y + circle_radius >= platform_y:
            circle_y = platform_y - circle_radius
            circle_dy = 0
            is_jumping = False
        elif circle_y >= screen_height:
            is_jumping = False
            
    # Update obstacle movement and spawning
    obstacle_removal_threshold = -screen_width  # Remove obstacles off-screen
    for i in range(len(obstacles) - 1, -1, -1):
        obstacle = obstacles[i]
        obstacle[1] -= obstacle_speed
        if obstacle[1] < obstacle_removal_threshold:
            obstacles.pop(i)
            lives -= 1
            if lives == 0:
                running = False

    # Spawn new obstacles less frequently (adjust probability as needed)
    if random.random() < 0.02:
        obstacle_type = random.choice(obstacle_shapes)
        obstacle_color = random.choice(obstacle_colors)
        if obstacle_type == "rectangle":
            obstacle_width = random.randint(20, 50)
            obstacle_height = random.randint(20, 30)
            obstacles.append([obstacle_type, platform_spawn_x, platform_y - obstacle_height, obstacle_width, obstacle_height, obstacle_color])
        elif obstacle_type == "triangle":
            obstacle_width = random.randint(30, 60)
            obstacle_height = random.randint(20, 30)
            obstacles.append([obstacle_type, platform_spawn_x, platform_y - obstacle_height, obstacle_width, obstacle_height, obstacle_color])
        elif obstacle_type == "square":
            obstacle_width = random.randint(20, 40)
            obstacle_height = obstacle_width
            obstacles.append([obstacle_type, platform_spawn_x, platform_y - obstacle_height, obstacle_width, obstacle_height, obstacle_color])

    # Apply gravity
    if is_jumping:
        circle_dy += circle_gravity
        circle_y += circle_dy
        if circle_y + circle_radius >= platform_y:
            circle_y = platform_y - circle_radius
            circle_dy = 0
            is_jumping = False
            last_jump_time = time.time()

    # Check for collision with platforms
    for platform_x in platforms:
        if (platform_x < circle_x < platform_x + platform_width and
            circle_y + circle_radius >= platform_y):
            circle_y = platform_y - circle_radius
            circle_dy = 0
            is_jumping = False
            last_jump_time = time.time()

    # Check for collision with obstacles
    for obstacle_x in obstacles:
        if (obstacle_x[1] - obstacle_radius < circle_x < obstacle_x[1] + obstacle_radius and
    obstacle_y - obstacle_radius < circle_y < obstacle_y + obstacle_radius):
            lives -= 1
            if lives == 0:
                running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the video feed as the background
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = np.transpose(frame, (1, 0, 2))  # Rearrange dimensions for Pygame
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

    # Draw the platforms
    for platform_x in platforms:
        pygame.draw.rect(screen, (0, 0, 0), (platform_x, platform_y, platform_width, platform_height))

    for obstacle in obstacles:
        obstacle_type, x, y, width, height, color = obstacle
        if obstacle_type == "rectangle":
            pygame.draw.rect(screen, color, (x, y, width, height))
        elif obstacle_type == "triangle":
            pygame.draw.polygon(screen, color, [(x, y), (x + width / 2, y - height), (x + width, y)])
        elif obstacle_type == "square":
            pygame.draw.rect(screen, color, (x, y, width, height))

    # Draw the player (circle)
    pygame.draw.circle(screen, (255, 0, 0), (circle_x, int(circle_y)), circle_radius)

    # Display the pose status, score, level, and lives
    pose_text = font.render(f'Pose: {pose_status}', True, (0, 0, 0))
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    level_text = font.render(f'Level: {level}', True, (0, 0, 0))
    lives_text = font.render(f'Lives: {lives}', True, (0, 0, 0))
    screen.blit(pose_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(level_text, (10, 70))
    screen.blit(lives_text, (10, 100))

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

