import pygame
import random
import sys
import json
import pathlib
from config import *
from db import ensure_table, save_score, top_scores, personal_best

# Initialization
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
CLOCK = pygame.time.Clock()
ASSETS_PATH = pathlib.Path(__file__).parent / "assets"
ensure_table()

# Settings
def load_settings():
    default = {"snake_color": GREEN, "grid": True, "sound": True}
    try:
        with open(ASSETS_PATH / "settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def save_settings(settings):
    with open(ASSETS_PATH / "settings.json", "w") as f:
        json.dump(settings, f)

settings = load_settings()

def toggle_setting(name):
    settings[name] = not settings.get(name, True)

def change_snake_color():
    colors = [GREEN, DARK_GREEN, RED, BLUE, YELLOW, CYAN, MAGENTA]
    current = settings.get("snake_color", GREEN)
    idx = colors.index(current) if current in colors else 0
    settings["snake_color"] = colors[(idx + 1) % len(colors)]

# Messages
current_message = ""
message_time = 0

def show_message(text):
    global current_message, message_time
    current_message = text
    message_time = pygame.time.get_ticks()

def draw_message():
    if current_message and pygame.time.get_ticks() - message_time < MESSAGE_DURATION:
        msg = BIG_FONT.render(current_message, True, WHITE)
        rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
        SCREEN.blit(msg, rect)

# UI Helpers
def button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(SCREEN, GRAY, rect)
    txt = FONT.render(text, True, WHITE)
    SCREEN.blit(txt, txt.get_rect(center=rect.center))
    if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        pygame.time.delay(150)
        return True
    return False

def draw_text_center(text, y, font=BIG_FONT, color=WHITE):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(WIDTH//2, y))
    SCREEN.blit(txt, rect)

# Game Objects
class Snake:
    def __init__(self):
        self.body = [(100, 100)]
        self.direction = (CELL_SIZE, 0)
        self.shield = False

    def move(self):
        x, y = self.body[0]
        dx, dy = self.direction
        self.body.insert(0, (x + dx, y + dy))
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def self_collision(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self, snake_body):
        self.spawn_time = pygame.time.get_ticks()
        self.weight = random.choice([1, 2, 3])
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        while True:
            x = random.randint(1, (WIDTH//CELL_SIZE)-2) * CELL_SIZE
            y = random.randint(1, (HEIGHT//CELL_SIZE)-2) * CELL_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > FOOD_EXPIRE_TIME

class PoisonFood(Food):
    def effect(self, snake):
        snake.body = snake.body[:-2]
        return len(snake.body) <= 0

class PowerUp:
    TYPES = ["speed", "slow", "shield"]
    COLORS = {"speed": YELLOW, "slow": CYAN, "shield": MAGENTA}

    def __init__(self, snake_body):
        self.type = random.choice(self.TYPES)
        self.spawn_time = pygame.time.get_ticks()
        self.position = Food(snake_body).position
        self.active = False

    def draw(self):
        pygame.draw.rect(SCREEN, self.COLORS[self.type], (*self.position, CELL_SIZE, CELL_SIZE))

class Obstacle:
    def __init__(self, snake_body):
        self.positions = []
        while len(self.positions) < 5:
            pos = (random.randint(1, (WIDTH//CELL_SIZE)-2) * CELL_SIZE,
                   random.randint(1, (HEIGHT//CELL_SIZE)-2) * CELL_SIZE)
            if pos not in snake_body and pos not in self.positions:
                self.positions.append(pos)

    def draw(self):
        for pos in self.positions:
            pygame.draw.rect(SCREEN, GRAY, (*pos, CELL_SIZE, CELL_SIZE))

# Username Input
def get_username():
    username = ""
    while True:
        SCREEN.fill(BLACK)
        txt = BIG_FONT.render("Enter Username: " + username, True, WHITE)
        rect = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
        SCREEN.blit(txt, rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

# Screens
def main_menu(username):
    while True:
        SCREEN.fill(BLACK)
        draw_text_center("SNAKE GAME", HEIGHT//4)
        if button("Play", WIDTH//2-100, HEIGHT//2-60, 200, 50):
            return "play"
        if button("Leaderboard", WIDTH//2-100, HEIGHT//2, 200, 50):
            return "leaderboard"
        if button("Settings", WIDTH//2-100, HEIGHT//2+60, 200, 50):
            return "settings"
        if button("Quit", WIDTH//2-100, HEIGHT//2+120, 200, 50):
            return "quit"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        pygame.display.update()
        CLOCK.tick(15)

def leaderboard_screen(username):
    while True:
        SCREEN.fill(BLACK)
        draw_text_center("LEADERBOARD", 50)
        scores = top_scores()
        start_y = 120
        for i, (user, score, level, ts) in enumerate(scores):
            line = f"{i+1}. {user} - Score: {score}, Level: {level}, {ts.strftime('%Y-%m-%d')}"
            txt = FONT.render(line, True, WHITE)
            SCREEN.blit(txt, (50, start_y + i*30))
        if button("Back", WIDTH//2-100, HEIGHT-80, 200, 50):
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        CLOCK.tick(15)

def settings_screen(username):
    global settings
    while True:
        SCREEN.fill(BLACK)
        draw_text_center("SETTINGS", 50)
        if button(f"Grid: {'ON' if settings.get('grid', True) else 'OFF'}", WIDTH//2-100, 120, 200, 50):
            toggle_setting('grid')
        if button(f"Sound: {'ON' if settings.get('sound', True) else 'OFF'}", WIDTH//2-100, 190, 200, 50):
            toggle_setting('sound')
        if button("Change Color", WIDTH//2-100, 260, 200, 50):
            change_snake_color()
        if button("Save and Back", WIDTH//2-100, HEIGHT-80, 200, 50):
            save_settings(settings)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        CLOCK.tick(15)

def game_over_screen_ui(score, level, username):
    best = personal_best(username)
    while True:
        SCREEN.fill(BLACK)
        draw_text_center("GAME OVER", HEIGHT//4)
        draw_text_center(f"Score: {score}", HEIGHT//4 + 60)
        draw_text_center(f"Level: {level}", HEIGHT//4 + 120)
        draw_text_center(f"Personal Best: {best}", HEIGHT//4 + 180)
        if button("Retry", WIDTH//2-100, HEIGHT//2+60, 200, 50):
            main(username)
            return
        if button("Quit", WIDTH//2-100, HEIGHT//2+120, 200, 50):
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        CLOCK.tick(15)

# Main Game Function
def main(username):
    snake = Snake()
    food = Food(snake.body)
    poison_food = None
    powerup = None
    obstacles = []
    score = 0
    level = 1
    foods_eaten = 0
    speed = BASE_SPEED
    last_powerup_time = 0

    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, CELL_SIZE):
                    snake.direction = (0, -CELL_SIZE)
                if event.key == pygame.K_DOWN and snake.direction != (0, -CELL_SIZE):
                    snake.direction = (0, CELL_SIZE)
                if event.key == pygame.K_LEFT and snake.direction != (CELL_SIZE, 0):
                    snake.direction = (-CELL_SIZE, 0)
                if event.key == pygame.K_RIGHT and snake.direction != (-CELL_SIZE, 0):
                    snake.direction = (CELL_SIZE, 0)

        # Move snake
        snake.move()
        head_x, head_y = snake.body[0]

        # Collisions
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or snake.self_collision():
            if not snake.shield:
                save_score(username, score, level)
                game_over_screen_ui(score, level, username)
                return
            else:
                snake.shield = False

        # Obstacles
        if level >= 3 and len(obstacles) < (level - 2):
            obstacles.append(Obstacle(snake.body))
        for obs in obstacles:
            for pos in obs.positions:
                pygame.draw.rect(SCREEN, GRAY, (*pos, CELL_SIZE, CELL_SIZE))
                if snake.body[0] == pos and not snake.shield:
                    save_score(username, score, level)
                    game_over_screen_ui(score, level, username)
                    return

        # Food logic
        if food.expired():
            food = Food(snake.body)
            show_message("FOOD EXPIRED")
        if snake.body[0] == food.position:
            score += food.weight
            foods_eaten += 1
            snake.grow()
            show_message(f"+{food.weight} POINTS")
            food = Food(snake.body)
            if foods_eaten % 3 == 0:
                level += 1
                show_message(f"LEVEL {level}")

        # Poison
        if not poison_food and random.random() < 0.03:
            poison_food = PoisonFood(snake.body)
        if poison_food:
            pygame.draw.rect(SCREEN, DARK_RED, (*poison_food.position, CELL_SIZE, CELL_SIZE))
            if snake.body[0] == poison_food.position:
                if poison_food.effect(snake):
                    save_score(username, score, level)
                    game_over_screen_ui(score, level, username)
                    return
                poison_food = None

        # Power-ups
        if not powerup and pygame.time.get_ticks() - last_powerup_time > 5000 and random.random() < 0.02:
            powerup = PowerUp(snake.body)
        if powerup:
            pygame.draw.rect(SCREEN, powerup.COLORS[powerup.type], (*powerup.position, CELL_SIZE, CELL_SIZE))
            if snake.body[0] == powerup.position:
                if powerup.type == "speed":
                    speed *= 2
                elif powerup.type == "slow":
                    speed = max(1, speed // 2)
                elif powerup.type == "shield":
                    snake.shield = True
                powerup = None
                last_powerup_time = pygame.time.get_ticks()

        # Draw snake
        for i, part in enumerate(snake.body):
            color = settings.get("snake_color", GREEN) if i == 0 else DARK_GREEN
            pygame.draw.rect(SCREEN, color, (*part, CELL_SIZE, CELL_SIZE))

        # Draw food
        color = RED if food.weight == 1 else BLUE if food.weight == 2 else WHITE
        pygame.draw.rect(SCREEN, color, (*food.position, CELL_SIZE, CELL_SIZE))

        # HUD & messages
        hud = FONT.render(f"Score: {score}  Level: {level}", True, WHITE)
        SCREEN.blit(hud, (10, 10))
        draw_message()

        # Grid
        if settings.get("grid", True):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(SCREEN, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(SCREEN, GRAY, (0, y), (WIDTH, y))

        pygame.display.update()
        CLOCK.tick(speed)

# Main loop
def run_game():
    username = get_username()
    current_screen = "main_menu"
    while True:
        if current_screen == "main_menu":
            current_screen = main_menu(username)
        elif current_screen == "play":
            main(username)
            current_screen = "main_menu"
        elif current_screen == "leaderboard":
            leaderboard_screen(username)
            current_screen = "main_menu"
        elif current_screen == "settings":
            settings_screen(username)
            current_screen = "main_menu"
        elif current_screen == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    run_game()
