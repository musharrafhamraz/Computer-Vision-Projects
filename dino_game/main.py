# import pygame
# import random

# # Initialize pygame
# pygame.init()

# # Game Constants
# WIDTH, HEIGHT = 800, 400
# GROUND_Y = HEIGHT - 60
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)

# # Load Assets
# dino_img = pygame.image.load("dino.png")  # Replace with actual images
# gift_img = pygame.image.load("gift.jpeg")
# girlfriend_img = pygame.image.load("dino_girlfriend.png")
# obstacle_img = pygame.image.load("obstacle.png")

# # Scale images
# dino_img = pygame.transform.scale(dino_img, (50, 50))
# gift_img = pygame.transform.scale(gift_img, (30, 30))
# girlfriend_img = pygame.transform.scale(girlfriend_img, (50, 50))
# obstacle_img = pygame.transform.scale(obstacle_img, (40, 50))

# # Sounds
# jump_sound = pygame.mixer.Sound("jump.mp3")  # Replace with actual sound files
# game_over_sound = pygame.mixer.Sound("gameover.mp3")
# background_music = "background.mp3"  # Replace with actual file
# pygame.mixer.music.load(background_music)
# pygame.mixer.music.play(-1)

# # Initialize screen
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()

# class Dino:
#     def __init__(self):
#         self.image = dino_img
#         self.x = 50
#         self.y = GROUND_Y
#         self.vel_y = 0
#         self.gravity = 1
#         self.jumping = False
    
#     def jump(self):
#         if not self.jumping:
#             self.vel_y = -15
#             self.jumping = True
#             jump_sound.play()
    
#     def update(self):
#         self.y += self.vel_y
#         self.vel_y += self.gravity
#         if self.y >= GROUND_Y:
#             self.y = GROUND_Y
#             self.jumping = False
    
#     def draw(self):
#         screen.blit(self.image, (self.x, self.y))

# class Obstacle:
#     def __init__(self):
#         self.image = obstacle_img
#         self.x = WIDTH
#         self.y = GROUND_Y
#         self.speed = 7
    
#     def update(self):
#         self.x -= self.speed
#         if self.x < -40:
#             self.x = WIDTH + random.randint(200, 400)
    
#     def draw(self):
#         screen.blit(self.image, (self.x, self.y))

# class Gift:
#     def __init__(self):
#         self.image = gift_img
#         self.x = random.randint(WIDTH // 2, WIDTH)
#         self.y = random.randint(100, GROUND_Y - 20)
    
#     def update(self):
#         self.x -= 5
    
#     def draw(self):
#         screen.blit(self.image, (self.x, self.y))

# def main():
#     run = True
#     dino = Dino()
#     obstacle = Obstacle()
#     gifts = []
#     score = 0
#     collected_gifts = 0
    
#     while run:
#         screen.fill(WHITE)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                 dino.jump()
        
#         dino.update()
#         obstacle.update()
        
#         if score % 1000 == 0 and score > 0:
#             gifts.append(Gift())
        
#         for gift in gifts[:]:
#             gift.update()
#             if dino.x < gift.x < dino.x + 50 and dino.y < gift.y < dino.y + 50:
#                 gifts.remove(gift)
#                 collected_gifts += 1
        
#         if dino.x < obstacle.x < dino.x + 50 and dino.y > obstacle.y - 20:
#             game_over_sound.play()
#             pygame.time.delay(1000)
#             if collected_gifts >= 10:
#                 screen.fill(WHITE)
#                 screen.blit(girlfriend_img, (WIDTH//2 - 50, HEIGHT//2 - 50))
#                 pygame.display.flip()
#                 pygame.time.delay(2000)
#             else:
#                 screen.fill(WHITE)
#                 font = pygame.font.SysFont("Arial", 30)
#                 text = font.render("Stay single for one more year!", True, RED)
#                 screen.blit(text, (WIDTH//2 - 200, HEIGHT//2 - 20))
#                 pygame.display.flip()
#                 pygame.time.delay(2000)
#             run = False
        
#         dino.draw()
#         obstacle.draw()
#         for gift in gifts:
#             gift.draw()
        
#         pygame.display.update()
#         clock.tick(30)
#         score += 10
    
#     pygame.quit()

# if __name__ == "__main__":
#     main()
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
DINO_SPEED = 5
OBSTACLE_SPEED = 5  # Speed of obstacles
STAR_SPEED = 3  # Speed of stars
STAR_GOAL = 10
HALF_WAY = 6
GRAVITY = 1
JUMP_STRENGTH = -15
FONT = pygame.font.Font(None, 36)

# Load Images
dino_img = pygame.image.load("dino.png")
dino_gf_img = pygame.image.load("dino_girlfriend.png")
another_dino_img = pygame.image.load("dino_villan.png")
gift_img = pygame.image.load("gift.jpeg")
obstacle_img = pygame.image.load("obstacle.png")
background_img = pygame.image.load("background.jpg")

# Resize Images
dino_img = pygame.transform.scale(dino_img, (100, 100))
dino_gf_img = pygame.transform.scale(dino_gf_img, (100, 100))
another_dino_img = pygame.transform.scale(another_dino_img, (100, 100))
gift_img = pygame.transform.scale(gift_img, (50, 50))
obstacle_img = pygame.transform.scale(obstacle_img, (60, 60))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load Sounds
pygame.mixer.music.load("background.mp3")
jump_sound = pygame.mixer.Sound("jump.mp3")
collect_sound = pygame.mixer.Sound("coin.mp3")
fail_sound = pygame.mixer.Sound("gameover.mp3")
love_sound = pygame.mixer.Sound("love.mp3")

# Play Background Music
pygame.mixer.music.play(-1)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

dino_x, dino_y = 50, HEIGHT - 100
dino_velocity = 0
gf_x, gf_y = WIDTH - 100, HEIGHT - 100
stars_collected = 0
game_over = False
message_displayed = False
stars = []
obstacles = []

def restart_game():
    global dino_x, dino_y, dino_velocity, stars_collected, game_over, message_displayed, stars, obstacles
    dino_x, dino_y = 50, HEIGHT - 100
    dino_velocity = 0
    stars_collected = 0
    game_over = False
    message_displayed = False
    stars = [[random.randint(100, WIDTH-50), random.randint(100, HEIGHT-100)] for _ in range(5)]
    obstacles = [[random.randint(200, WIDTH-50), HEIGHT-60] for _ in range(3)]

# Generate initial stars and obstacles
restart_game()

running = True
while running:
    screen.blit(background_img, (0, 0))


    # Move and display stars
    for star in stars:
        star[0] -= STAR_SPEED  # Move star to the left
        # if star[0] < -50:  # Reset when off-screen
        #     star[0] = random.randint(WIDTH, WIDTH + 100)
        #     star[1] = random.randint(100, HEIGHT - 100)
        # screen.blit(gift_img, (star[0], star[1]))

    # Move and display obstacles
    for obs in obstacles:
        obs[0] -= OBSTACLE_SPEED  # Move obstacle to the left
        # if obs[0] < -60:  # Reset when off-screen
        #     obs[0] = random.randint(WIDTH, WIDTH + 200)
        # screen.blit(obstacle_img, (obs[0], obs[1]))
    
    # Display Dino and collected stars
    screen.blit(dino_img, (dino_x, dino_y))
    score_text = FONT.render(f"Stars: {stars_collected}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    # Display message when 6 stars are collected
    if stars_collected == HALF_WAY and not message_displayed:
        message_text = FONT.render("Your Valentine is waiting...", True, (255, 0, 0))
        screen.blit(message_text, (WIDTH//4, HEIGHT//2))
        message_displayed = True  # Add this line
        
    # Display stars
    for star in stars:
        screen.blit(gift_img, (star[0], star[1]))
    
    # Display obstacles
    for obs in obstacles:
        screen.blit(obstacle_img, (obs[0], obs[1]))
    
    # Check collision with stars
    for star in stars[:]:
        star_rect = pygame.Rect(star[0], star[1], 50, 50)
        dino_rect = pygame.Rect(dino_x, dino_y, 100, 100)
        if dino_rect.colliderect(star_rect):
            stars.remove(star)
            stars_collected += 1
            collect_sound.play()
            stars.append([random.randint(WIDTH, WIDTH + 100), random.randint(100, HEIGHT - 100)])
    
    # If 10 stars collected, show animation and collect gifts together
    if stars_collected >= STAR_GOAL and not love_sound_played:
        love_sound.play()
        love_sound_played = True
        screen.blit(dino_gf_img, (gf_x, gf_y))
        love_text = FONT.render("Dino and GF are collecting gifts together!", True, (0, 0, 255))
        screen.blit(love_text, (WIDTH//4, HEIGHT//2))
        love_sound.play()
    
    # If Dino collides with obstacle
    for obs in obstacles:
        obs_rect = pygame.Rect(obs[0], obs[1], 60, 60)
        dino_rect = pygame.Rect(dino_x, dino_y, 100, 100)
        if dino_rect.colliderect(obs_rect):
            game_over = True
            fail_sound.play()
    
    if game_over:
        fail_text = FONT.render("Dino failed! GF found another Dino...", True, (255, 0, 0))
        screen.blit(fail_text, (WIDTH//4, HEIGHT//2))
        screen.blit(another_dino_img, (gf_x, gf_y))
        retry_text = FONT.render("Try Again? Press R", True, (0, 0, 0))
        screen.blit(retry_text, (WIDTH//4, HEIGHT//2 + 50))
    
    pygame.display.update()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()
            if event.key == pygame.K_SPACE and dino_y == HEIGHT - 100:
                dino_velocity = JUMP_STRENGTH
                jump_sound.play()
    
    # Apply gravity
    dino_velocity += GRAVITY
    dino_y += dino_velocity
    if dino_y > HEIGHT - 100:
        dino_y = HEIGHT - 100
    
    clock.tick(30)

pygame.quit()

