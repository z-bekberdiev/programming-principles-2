import pygame
import persistence

pygame.init()

FONT = pygame.font.SysFont("SF Mono", 24)
BIG_FONT = pygame.font.SysFont("SF Mono", 48)

def draw_centered_text(screen, text, y, font, color=(255,255,255)):
    text_surf = font.render(text, True, color)
    x = screen.get_width() // 2 - text_surf.get_width() // 2
    screen.blit(text_surf, (x, y))

def draw_button(screen, text, rect, color=(70,70,70), text_color=(255,255,255)):
    pygame.draw.rect(screen, color, rect)
    label = FONT.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def main_menu(screen):
    WIDTH = screen.get_size()[0]
    buttons = {
        "Play": pygame.Rect(WIDTH//2-100, 200, 200, 50),
        "Leaderboard": pygame.Rect(WIDTH//2-100, 300, 200, 50),
        "Settings": pygame.Rect(WIDTH//2-100, 400, 200, 50),
        "Quit": pygame.Rect(WIDTH//2-100, 500, 200, 50)
    }
    return buttons

def settings_screen(screen, settings):
    screen.fill((30, 30, 30))
    WIDTH = screen.get_size()[0]
    FONT = pygame.font.SysFont("SF Mono", 28)
    BIG_FONT = pygame.font.SysFont("SF Mono", 48)
    
    # Title
    title_surf = BIG_FONT.render("Settings", True, (255, 215, 0))
    screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))
    
    # Options list
    options = [
        f"Sound: {'On' if settings['sound'] else 'Off'} (Press S to toggle)",
        f"Difficulty: {settings['difficulty']} (Press D to toggle)",
        f"Car Color: {settings['car_color']} (Press C to randomize)",
        "Press B to go Back"
    ]
    
    start_y = 200
    spacing = 60
    
    for i, text in enumerate(options):
        text_surf = FONT.render(text, True, (255, 255, 255))
        x = WIDTH//2 - text_surf.get_width()//2
        y = start_y + i*spacing
        screen.blit(text_surf, (x, y))

def game_over_screen(screen, score, coins, distance):
    # Game Over Screen
    screen.fill((30,30,30))
    draw_centered_text(screen, "GAME OVER", screen.get_height()//2 - 100, BIG_FONT, (255, 0, 0))
    draw_centered_text(screen, f"Score: {score}", screen.get_height()//2 - 30, FONT)
    draw_centered_text(screen, f"Coins: {coins}", screen.get_height()//2, FONT)
    draw_centered_text(screen, f"Distance: {distance}", screen.get_height()//2 + 30, FONT)
    draw_centered_text(screen, "Press R to Retry or Q to Quit", screen.get_height()//2 + 80, FONT)

def leaderboard_screen(screen):
    leaderboard = persistence.load_leaderboard()
    screen.fill((20,20,40))
    screen.fill((20,20,40))
    draw_centered_text(screen, "Leaderboard", 50, BIG_FONT, (255,215,0))

    start_y = 150
    for i, entry in enumerate(leaderboard):
        line = f"{i+1}. {entry['name']} - {entry['score']} pts - {entry['distance']}m"
        draw_centered_text(screen, line, start_y + i*40, FONT)