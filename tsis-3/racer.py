import pygame
import random
import sys
import persistence
import ui

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (220,50,50)
GREEN = (50,200,50)
YELLOW = (255,215,0)
ORANGE = (255,165,0)
MAGENTA = (255,0,255)
GRAY = (100,100,100)
BLUE = (50,150,255)

settings = persistence.load_settings()
FONT = pygame.font.SysFont("SF Mono", 24)

# --- Classes ---
class Player:
    def __init__(self, color=(50, 200, 50)):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT-80, 40, 60)
        self.base_speed = 6
        self.speed = self.base_speed
        self.color = color
        self.shield = False

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.shield:
            pygame.draw.rect(screen, (0, 255, 255), self.rect, 3)  # outline for shield

class Coin:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(50,WIDTH-50), random.randint(-600,-40), 25,25)
        self.value = random.choice([1,2,3])
        self.color = YELLOW if self.value==1 else ORANGE if self.value==2 else MAGENTA
        self.speed = random.randint(3,6)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, 12)

class Enemy:
    def __init__(self, speed):
        self.rect = pygame.Rect(random.randint(50,WIDTH-50), random.randint(-500,-40), 40,40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(50,WIDTH-50), random.randint(-500,-40), 50,20)
        self.type = random.choice(["oil","barrier"])
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        color = GRAY if self.type=="oil" else RED
        pygame.draw.rect(screen,color,self.rect)

class PowerUp:
    def __init__(self):
        self.type = random.choice(["nitro", "shield", "repair"])
        self.rect = pygame.Rect(
            random.randint(50, WIDTH - 50),
            random.randint(-500, -40),
            30, 30
        )
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        colors = {"nitro": (255, 165, 0), "shield": (0, 128, 255), "repair": (50, 205, 50)}
        pygame.draw.rect(screen, colors[self.type], self.rect)

# --- Reset ---
def reset_game():
    global player, coins, enemies, obstacles, powerups, score, coin_count, distance, enemy_speed, active_powerup, powerup_timer
    player = Player(settings['car_color'])
    coins=[]
    enemies=[]
    obstacles=[]
    powerups=[]
    score=0
    coin_count=0
    distance=0
    enemy_speed=4
    active_powerup=None
    powerup_timer=0

reset_game()

def username_entry_screen(screen):
    """
    Let the player type their username before starting the game.
    Returns the username string.
    """
    input_text = ""
    active = True
    clock = pygame.time.Clock()
    HEIGHT = screen.get_size()[1]
    font = pygame.font.SysFont("SF Mono", 32)
    
    while active:
        screen.fill((30,30,30))
        ui.draw_centered_text(screen, "Enter your name:", HEIGHT//2 - 60, font)
        ui.draw_centered_text(screen, input_text or "_", HEIGHT//2, font, YELLOW)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip() != "":
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 10:  # limit name length
                    if event.unicode.isalnum() or event.unicode in ("_", "-"):
                        input_text += event.unicode
        
        clock.tick(30)
    
    return input_text

player_name = username_entry_screen(screen)

# --- Events ---
COIN_EVENT = pygame.USEREVENT+1
ENEMY_EVENT = pygame.USEREVENT+2
OBSTACLE_EVENT = pygame.USEREVENT+3
POWERUP_EVENT = pygame.USEREVENT+4

pygame.time.set_timer(COIN_EVENT, 1200)
pygame.time.set_timer(ENEMY_EVENT, 1800)
pygame.time.set_timer(OBSTACLE_EVENT, 2500)
pygame.time.set_timer(POWERUP_EVENT, 7000)

active_powerup = None
powerup_start = 0
powerup_duration = 0

# --- Game Loop ---
game_state = "MENU"
running=True
while running:
    screen.fill((30,30,30))
    keys = pygame.key.get_pressed()
    mx,my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if game_state=="PLAYING":
            if event.type==COIN_EVENT: coins.append(Coin())
            if event.type==ENEMY_EVENT: enemies.append(Enemy(enemy_speed))
            if event.type==OBSTACLE_EVENT: obstacles.append(Obstacle())
            if event.type==POWERUP_EVENT: powerups.append(PowerUp())
        
        if game_state=="GAME_OVER":
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r: reset_game(); game_state="PLAYING"
                if event.key==pygame.K_q: running=False

        if game_state=="MENU":
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                buttons = ui.main_menu(screen)
                for name, rect in buttons.items():
                    if rect.collidepoint(mx,my):
                        if name=="Play":
                            game_state="PLAYING"
                            reset_game()
                        elif name=="Leaderboard": game_state="LEADERBOARD"
                        elif name=="Settings": game_state="SETTINGS"
                        elif name=="Quit": running=False

        if game_state=="SETTINGS":
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s: settings["sound"]=not settings["sound"]
                if event.key==pygame.K_d: settings["difficulty"]="Hard" if settings["difficulty"]=="Normal" else "Normal"
                if event.key==pygame.K_c: settings["car_color"]=[random.randint(0,255) for _ in range(3)]
                if event.key==pygame.K_b: persistence.save_settings(settings); game_state="MENU"

        if game_state=="LEADERBOARD":
            if event.type==pygame.KEYDOWN and event.key==pygame.K_b:
                game_state="MENU"

    # --- Gameplay ---
    if game_state=="PLAYING":
        player.move(keys)
        distance += 1

        # Coins
        for coin in coins[:]:
            coin.update()
            if player.rect.colliderect(coin.rect):
                score += coin.value
                coin_count += 1
                coins.remove(coin)
                if coin_count%5==0: enemy_speed+=1
            elif coin.rect.top>HEIGHT: coins.remove(coin)

        # Enemies
        for enemy in enemies[:]:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                if player.shield: player.shield=False; enemies.remove(enemy)
                else: persistence.add_score(player_name, score, distance); game_state="GAME_OVER"
            elif enemy.rect.top>HEIGHT: enemies.remove(enemy)

        # Obstacles
        for obs in obstacles[:]:
            obs.update()
            if player.rect.colliderect(obs.rect):
                if player.shield: player.shield=False; obstacles.remove(obs)
                else: persistence.add_score(player_name, score, distance); game_state="GAME_OVER"
            elif obs.rect.top>HEIGHT: obstacles.remove(obs)

        # --- Check collisions with power-ups ---
        for pu in powerups[:]:
            pu.update()
            if player.rect.colliderect(pu.rect):
                if not active_powerup:
                    active_powerup = pu.type
                    powerup_start = pygame.time.get_ticks()

                    if pu.type == "nitro":
                        powerup_duration = random.randint(3000, 5000)  # 3-5 seconds
                        player.speed = player.base_speed * 2

                    elif pu.type == "shield":
                        player.shield = True
                        powerup_duration = 0  # lasts until hit

                    elif pu.type == "repair":
                        # instant effect example: remove one obstacle
                        if obstacles:
                            obstacles.pop(0)
                        active_powerup = None  # repair is instant
                        powerup_duration = 0

                powerups.remove(pu)
            elif pu.rect.top > HEIGHT:
                powerups.remove(pu)

        # --- Nitro expires ---
        if active_powerup == "nitro":
            if pygame.time.get_ticks() - powerup_start > powerup_duration:
                active_powerup = None
                player.speed = player.base_speed

        # --- Shield removed on collision ---
        if active_powerup == "shield" and not player.shield:
            active_powerup = None

        # Draw
        player.draw()
        for coin in coins: coin.draw()
        for enemy in enemies: enemy.draw()
        for obs in obstacles: obs.draw()
        for pu in powerups: pu.draw()

        # Draw in-game HUD (top-left corner)
        hud_x, hud_y = 10, 10
        line_height = 30

        screen.blit(FONT.render(f"Score: {score}", True, WHITE), (hud_x, hud_y))
        screen.blit(FONT.render(f"Coins: {coin_count}", True, WHITE), (hud_x, hud_y + line_height))
        screen.blit(FONT.render(f"Distance: {distance}", True, WHITE), (hud_x, hud_y + 2*line_height))
        if active_powerup:
            screen.blit(FONT.render(f"Power-Up: {active_powerup}", True, WHITE), (hud_x, hud_y + 3*line_height))

    elif game_state=="GAME_OVER":
        ui.game_over_screen(screen, score, coin_count, distance)

    elif game_state=="MENU":
        screen.fill((50,50,50))
        buttons = ui.main_menu(screen)
        for text, rect in buttons.items():
            ui.draw_button(screen,text,rect)

    elif game_state=="SETTINGS":
        ui.settings_screen(screen, settings)

    elif game_state=="LEADERBOARD":
        ui.leaderboard_screen(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()