import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

flag = True

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont("SF Mono", 20)
big_font = pygame.font.SysFont("SF Mono", 40)

# Message system
current_message = ""
message_time = 0
MESSAGE_DURATION = 1000

def show_message(text):
    # Show temporary message on screen
    global current_message, message_time
    current_message = text
    message_time = pygame.time.get_ticks()

def draw_message():
    # Draw message if it is still active
    if current_message:
        if pygame.time.get_ticks() - message_time < MESSAGE_DURATION:
            msg = big_font.render(current_message, True, WHITE)
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(msg, rect)

# Game over screen
def game_over_screen(text):
    global flag
    flag = False
    screen.fill(BLACK)
    msg = big_font.render(text, True, WHITE)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.update()
    pygame.time.delay(3000)

# Snake
class Snake:
    def __init__(self):
        self.body = [(100, 100)]
        self.direction = (CELL_SIZE, 0)

    def move(self):
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = (x + dx, y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def self_collision(self):
        return self.body[0] in self.body[1:]

# Food
class Food:
    def __init__(self, snake_body):
        self.spawn_time = pygame.time.get_ticks()
        self.weight = random.choice([1, 2, 3])
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        while True:
            x = random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE
            y = random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 5000 and flag

# Game variables
snake = Snake()
food = Food(snake.body)

score = 0
level = 1
foods_eaten = 0
base_speed = 8

running = True

# Main loop
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
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

    # Wall collision (game over)
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over_screen("GAME OVER")
        running = False

    # Self collision (game over)
    if snake.self_collision():
        game_over_screen("GAME OVER")
        running = False

    # Food expiration
    if food.expired():
        food = Food(snake.body)
        show_message("FOOD EXPIRED")

    # Food eaten
    if snake.body[0] == food.position:
        score += food.weight
        foods_eaten += 1
        snake.grow()

        show_message(f"+{food.weight} POINTS")

        food = Food(snake.body)

        # Level system
        if foods_eaten % 3 == 0:
            level += 1
            show_message(f"LEVEL {level}")

    # Draw food
    color = RED if food.weight == 1 else BLUE if food.weight == 2 else WHITE
    pygame.draw.rect(screen, color, (*food.position, CELL_SIZE, CELL_SIZE))

    # Draw snake
    for i, part in enumerate(snake.body):
        pygame.draw.rect(screen, GREEN if i == 0 else DARK_GREEN,
                         (*part, CELL_SIZE, CELL_SIZE))

    # Speed increases with level
    speed = base_speed + (level - 1) * 2
    clock.tick(speed)

    # HUD (score + level)
    hud = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(hud, (10, 10))

    # Draw messages
    draw_message()

    pygame.display.update()

pygame.quit()
sys.exit()