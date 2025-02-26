
import cv2
import mediapipe as mp
import numpy as np
import random
import pygame

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load images with transparency handling
def load_image_with_alpha(path, width, height):
    """Load an image and ensure it has an alpha channel."""
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 3:  # Add alpha channel if missing
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    return cv2.resize(img, (width, height))

# Character properties
CHARACTER_IMAGE_PATH = "character1.png"  # Replace with your image path
character_image = load_image_with_alpha(CHARACTER_IMAGE_PATH, 80, 80)
character_width, character_height = 80, 80
character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - character_height - 10

# Obstacle properties
OBSTACLE_IMAGE_PATHS = ["enemy.png", "enemy1.png", "enemy2.png",]  # Replace with your paths
obstacle_images = [load_image_with_alpha(path, 80, 80) for path in OBSTACLE_IMAGE_PATHS]
obstacles = []
OBSTACLE_SPEED = 7
SPAWN_RATE = 40  # Spawn a new obstacle every 30 frames

# Projectile properties
projectiles = []
PROJECTILE_SPEED = 7

# Game variables
score = 0
game_over = False

# Initialize Pygame for background music
pygame.mixer.init()
BACKGROUND_MUSIC_PATH = "music.mp3"  # Replace with your music file path
pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Function to spawn a new obstacle
def spawn_obstacle():
    x = random.randint(0, SCREEN_WIDTH - 50)
    obstacle_image = random.choice(obstacle_images)
    obstacles.append([x, -50, obstacle_image])

# Function to check collision between two rectangles
def check_collision(rect1, rect2):
    return not (rect1[0] + rect1[2] <= rect2[0] or
                rect1[0] >= rect2[0] + rect2[2] or
                rect1[1] + rect1[3] <= rect2[1] or
                rect1[1] >= rect2[1] + rect2[3])

# Main game loop
cap = cv2.VideoCapture(0)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a more natural feel
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Extract hand landmarks
    # Extract hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the position of the index finger tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            index_x = int(index_finger_tip.x * w)
            index_y = int(index_finger_tip.y * h)

            # Map the index finger position to the game screen
            character_x = int((index_x / w) * SCREEN_WIDTH)
            character_y = int((index_y / h) * SCREEN_HEIGHT)

            # Clamp the character's position to stay within the screen bounds
            character_x = max(0, min(character_x, SCREEN_WIDTH - character_width))
            character_y = max(0, min(character_y, SCREEN_HEIGHT - character_height))

            # Draw the hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        # If no hand is detected, freeze the character's position
        character_x = max(0, min(character_x, SCREEN_WIDTH - character_width))
        character_y = max(0, min(character_y, SCREEN_HEIGHT - character_height))

    # Resize the camera feed to match the game screen dimensions
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Update obstacles
    if frame_count % SPAWN_RATE == 0:
        spawn_obstacle()
    new_obstacles = []
    for obstacle in obstacles:
        obstacle[1] += OBSTACLE_SPEED  # Move the obstacle down
        if obstacle[1] < SCREEN_HEIGHT:  # Keep only visible obstacles
            new_obstacles.append(obstacle)
            # Check for collision with the character
            if check_collision([character_x, character_y, character_width, character_height],
                            [obstacle[0], obstacle[1], 80, 80]):  # Use 80x80 for obstacle size
                game_over = True
            # Randomly spawn projectiles from obstacles
            if random.random() < 0.02:  # 2% chance per frame to spawn a projectile
                projectiles.append([obstacle[0] + 25, obstacle[1] + 50, random.choice(["circle", "square"])])
        else:
            score += 1  # Increment score for dodging an obstacle
    obstacles = new_obstacles

    # Update projectiles
    new_projectiles = []
    for projectile in projectiles:
        projectile[1] += PROJECTILE_SPEED  # Move the projectile down
        if projectile[1] < SCREEN_HEIGHT:  # Keep only visible projectiles
            new_projectiles.append(projectile)

            # Check for collision with the character
            if check_collision([character_x, character_y, character_width, character_height],
                               [projectile[0] - 10, projectile[1], 20, 20]):
                game_over = True
        else:
            score += 1  # Increment score for dodging a projectile
    projectiles = new_projectiles

    # Draw the character
    # Draw the character
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)  # Convert to BGRA for transparency

    # Ensure the character image has the correct dimensions
    assert character_image.shape[:2] == (character_height, character_width), \
        f"Character image dimensions mismatch: {character_image.shape[:2]} != ({character_height}, {character_width})"

    # Calculate alpha blending factors
    alpha_s = character_image[:, :, 3] / 255.0  # Alpha channel of the character image
    alpha_l = 1.0 - alpha_s  # Inverse alpha

    # Blend the character image onto the frame
    for c in range(3):  # Iterate over BGR channels
        frame[character_y:character_y + character_height, character_x:character_x + character_width, c] = (
            alpha_s * character_image[:, :, c] +
            alpha_l * frame[character_y:character_y + character_height, character_x:character_x + character_width, c]
        )

    # Update the alpha channel of the frame
    frame[character_y:character_y + character_height, character_x:character_x + character_width, 3] = \
        character_image[:, :, 3]

    # Draw the obstacles
    for obstacle in obstacles:
        x, y, img = obstacle
        # Clamp the obstacle's position to stay within the screen bounds
        x = max(0, min(x, SCREEN_WIDTH - 80))  # Use 80 instead of 50
        y = max(0, min(y, SCREEN_HEIGHT - 80))  # Use 80 instead of 50

        # Ensure the obstacle image has the correct dimensions
        assert img.shape[:2] == (80, 80), f"Obstacle image dimensions mismatch: {img.shape[:2]} != (80, 80)"

        # Calculate alpha blending factors
        alpha_s = img[:, :, 3] / 255.0  # Alpha channel of the obstacle image
        alpha_l = 1.0 - alpha_s  # Inverse alpha

        # Blend the obstacle image onto the frame
        for c in range(3):  # Iterate over BGR channels
            frame[y:y + 80, x:x + 80, c] = (
                alpha_s * img[:, :, c] +
                alpha_l * frame[y:y + 80, x:x + 80, c]
            )

        # Update the alpha channel of the frame
        frame[y:y + 80, x:x + 80, 3] = img[:, :, 3]

    # Draw the projectiles
    for projectile in projectiles:
        x, y, shape = projectile

        # Clamp the projectile's position to stay within the screen bounds
        x = max(0, min(x, SCREEN_WIDTH))
        y = max(0, min(y, SCREEN_HEIGHT))

        if shape == "circle":
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
        elif shape == "square":
            cv2.rectangle(frame, (x - 10, y - 10), (x + 10, y + 10), (0, 255, 0), -1)

    # Display the score
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Check for game over
    if game_over:
        cv2.putText(frame, "GAME OVER", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        cv2.imshow("Finger Dodge", frame)
        if cv2.waitKey(2000) & 0xFF == ord('q'):  # Wait for 2 seconds before exiting
            break
        break

    # Display the game screen
    cv2.imshow("Finger Dodge", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()