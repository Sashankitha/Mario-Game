import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 25

# Paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
cactus_img_path = os.path.join(ASSETS_DIR, "cactus_bricks.png")
fire_img_path = os.path.join(ASSETS_DIR, "fire_bricks.png")
dragon_img_path = os.path.join(ASSETS_DIR, "dragon.png")
fireball_img_path = os.path.join(ASSETS_DIR, "fireball.png")
mario_img_path = os.path.join(ASSETS_DIR, "maryo.png")
theme_music_path = os.path.join(ASSETS_DIR, "mario_theme.wav")
death_sound_path = os.path.join(ASSETS_DIR, "mario_dies.wav")
start_img_path = os.path.join(ASSETS_DIR, "start.png")
end_img_path = os.path.join(ASSETS_DIR, "end.png")

# Helper function to load images with placeholders
def load_image(path, size=None):
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except FileNotFoundError:
        print(f"FileNotFoundError: {path} not found. Using a placeholder.")
        placeholder = pygame.Surface(size if size else (100, 100))
        placeholder.fill((128, 128, 128))
        return placeholder

# Load assets with placeholders
cactus_img = load_image(cactus_img_path)
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0

fire_img = load_image(fire_img_path)
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0

CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mario')

# Top Score Class
class Topscore:
    def __init__(self):
        self.high_score = 0

    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()

# Dragon Class
class Dragon:
    dragon_velocity = 10

    def __init__(self):
        self.dragon_img = load_image(dragon_img_path)
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width -= 10
        self.dragon_img_rect.height -= 10
        self.dragon_img_rect.top = WINDOW_HEIGHT / 2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= self.dragon_velocity
        elif self.down:
            self.dragon_img_rect.top += self.dragon_velocity

# Flames Class
class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = load_image(fireball_img_path, (20, 20))
        self.flames_img_rect = self.flames.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30

    def update(self):
        canvas.blit(self.flames, self.flames_img_rect)
        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity

# Mario Class
class Mario:
    velocity = 10

    def __init__(self):
        self.mario_img = load_image(mario_img_path)
        self.mario_img_rect = self.mario_img.get_rect()
        self.mario_img_rect.left = 20
        self.mario_img_rect.top = WINDOW_HEIGHT / 2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.mario_img, self.mario_img_rect)
        if self.mario_img_rect.top <= cactus_img_rect.bottom:
            game_over()
        if self.mario_img_rect.bottom >= fire_img_rect.top:
            game_over()
        if self.up:
            self.mario_img_rect.top -= 10
        if self.down:
            self.mario_img_rect.bottom += 10

# Game Over Function
def game_over():
    try:
        music = pygame.mixer.Sound(death_sound_path)
        music.play()
    except FileNotFoundError:
        print(f"Sound file {death_sound_path} not found. Skipping game over sound.")
    topscore.top_score(SCORE)
    game_over_img = load_image(end_img_path)
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

# Start Game Function
def start_game():
    canvas.fill(BLACK)
    start_img = load_image(start_img_path)
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

# Main Game Loop
def game_loop():
    global dragon
    dragon = Dragon()
    flames = Flames()
    mario = Mario()
    add_new_flame_counter = 0
    global SCORE
    SCORE = 0
    flames_list = []

    try:
        pygame.mixer.music.load(theme_music_path)
        pygame.mixer.music.play(-1, 0.0)
    except FileNotFoundError:
        print(f"Music file {theme_music_path} not found. Skipping background music.")

    while True:
        canvas.fill(BLACK)
        dragon.update()
        add_new_flame_counter += 1

        if add_new_flame_counter == ADD_NEW_FLAME_RATE:
            add_new_flame_counter = 0
            flames_list.append(Flames())
        for f in flames_list:
            if f.flames_img_rect.left <= 0:
                flames_list.remove(f)
            f.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mario.up = True
                    mario.down = False
                elif event.key == pygame.K_DOWN:
                    mario.down = True
                    mario.up = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    mario.up = False
                    mario.down = True
                elif event.key == pygame.K_DOWN:
                    mario.down = True
                    mario.up = False

        canvas.blit(cactus_img, cactus_img_rect)
        canvas.blit(fire_img, fire_img_rect)
        mario.update()

        pygame.display.update()
        CLOCK.tick(FPS)

# Start the Game
start_game()
 