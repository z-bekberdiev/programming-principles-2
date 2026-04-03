import pygame
import sys

def start_game() -> None:
    pygame.init()
    width, height = 500, 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()
    x, y = width // 2, height // 2
    radius = 25
    shift = 20
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if y - shift - radius > 0:
                        y -= shift
                elif event.key == pygame.K_DOWN:
                    if y + shift + radius < height:
                        y += shift
                elif event.key == pygame.K_LEFT:
                    if x - shift - radius > 0:
                        x -= shift
                elif event.key == pygame.K_RIGHT:
                    if x + shift + radius < width:
                        x += shift
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_game()
