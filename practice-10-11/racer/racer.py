import pygame
import random
import sys

# Initial setup
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("SF Mono", 24)

# Default colors
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 215, 0)

# Player
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 80, 40, 60)
        self.speed = 6

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Coin
class Coin:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(50, WIDTH - 50),
            random.randint(-600, -40),
            25,
            25
        )

        # Weighted values
        self.value = random.choice([1, 2, 3])

        # Color depends on value
        if self.value == 1:
            self.color = YELLOW
        elif self.value == 2:
            self.color = (255, 165, 0)
        else:
            self.color = (255, 0, 255)

        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, 12)

# Enemy
class Enemy:
    def __init__(self, speed):
        self.rect = pygame.Rect(
            random.randint(50, WIDTH - 50),
            random.randint(-500, -40),
            40,
            40
        )
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Reset function
def reset_game():
    global player, coins, enemies, score, coin_count, enemy_speed
    player = Player()
    coins = []
    enemies = []
    score = 0
    coin_count = 0
    enemy_speed = 4

reset_game()

# Game variables
game_state = "PLAYING"
final_score = 0

COIN_EVENT = pygame.USEREVENT + 1
ENEMY_EVENT = pygame.USEREVENT + 2

pygame.time.set_timer(COIN_EVENT, 1200)
pygame.time.set_timer(ENEMY_EVENT, 1800)

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "PLAYING"

                if event.key == pygame.K_q:
                    running = False

        # Spawning (only playing)
        if game_state == "PLAYING":
            if event.type == COIN_EVENT:
                coins.append(Coin())

            if event.type == ENEMY_EVENT:
                enemies.append(Enemy(enemy_speed))

    # Game logic
    if game_state == "PLAYING":

        keys = pygame.key.get_pressed()
        player.move(keys)

        # Coins
        for coin in coins[:]:
            coin.update()

            if player.rect.colliderect(coin.rect):
                score += coin.value
                coin_count += 1
                coins.remove(coin)

                # Increase difficulty every 5 coins
                if coin_count % 5 == 0:
                    enemy_speed += 1

            elif coin.rect.top > HEIGHT:
                coins.remove(coin)

        # Enemies
        for enemy in enemies[:]:
            enemy.update()

            if player.rect.colliderect(enemy.rect):
                final_score = score
                game_state = "GAME_OVER"

            elif enemy.rect.top > HEIGHT:
                enemies.remove(enemy)

    # Draw game
    if game_state == "PLAYING":

        player.draw()

        for coin in coins:
            coin.draw()

        for enemy in enemies:
            enemy.draw()

        # UI (top right)
        screen.blit(FONT.render(f"Score: {score}", True, WHITE), (WIDTH - 140, 10))
        screen.blit(FONT.render(f"Coins: {coin_count}", True, WHITE), (WIDTH - 140, 40))

    # Game over screen
    elif game_state == "GAME_OVER":

        big_font = pygame.font.SysFont("SF Mono", 64)
        mid_font = pygame.font.SysFont("SF Mono", 28)

        game_over_text = big_font.render("GAME OVER", True, RED)
        score_text = mid_font.render(f"Final Score: {final_score}", True, WHITE)
        restart_text = mid_font.render("Press R to Restart or Q to Quit", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()