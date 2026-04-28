import pygame

# Screen Settings
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 20

# Colors
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
GREEN       = (0, 255, 0)
DARK_GREEN  = (0, 180, 0)
RED         = (255, 0, 0)
DARK_RED    = (139, 0, 0)
BLUE        = (0, 0, 255)
YELLOW      = (255, 255, 0)
CYAN        = (0, 255, 255)
MAGENTA     = (255, 0, 255)
GRAY        = (128, 128, 128)

# Fonts
pygame.font.init()
FONT       = pygame.font.SysFont("SF Mono", 20)
BIG_FONT   = pygame.font.SysFont("SF Mono", 40)

# Game Settings
BASE_SPEED        = 8
FOOD_EXPIRE_TIME  = 5000  # ms
MESSAGE_DURATION  = 1000  # ms
POWERUP_DURATION  = 5000  # ms active effect
POWERUP_SPAWN_TIME= 8000  # ms on field

# Database Config
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '123123',
    'port': 5432
}