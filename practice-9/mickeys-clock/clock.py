import pygame
import sys
from pathlib import Path
from datetime import datetime

def start_application() -> None:
    pygame.init()
    width = 700
    height = 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    mickey = pygame.transform.scale(pygame.image.load(f'{Path(__file__).parent}/images/dial.jpg').convert_alpha(), (600, 600))
    hand = pygame.transform.scale(pygame.image.load(f'{Path(__file__).parent}/images/hand.png').convert_alpha(), (500, 500))
    center = (width // 2, height // 2)

    def rotate_hand(image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=center)
        return rotated, rect

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        now = datetime.now()
        minutes = now.minute
        seconds = now.second
        minute_angle = -(minutes / 60) * 360
        second_angle = -(seconds / 60) * 360
        rotated_minute, minute_rect = rotate_hand(hand, minute_angle)
        rotated_second, second_rect = rotate_hand(hand, second_angle)
        screen.fill((255, 255, 255))
        mickey_rect = mickey.get_rect(center=center)
        screen.blit(mickey, mickey_rect)
        screen.blit(rotated_minute, minute_rect)
        screen.blit(rotated_second, second_rect)
        font = pygame.font.SysFont(None, 40)
        time_text = f"{minutes:02}:{seconds:02}"
        text_surface = font.render(time_text, True, (0, 0, 0))
        screen.blit(text_surface, (width // 2 - 40, height - 35))
        pygame.display.flip()
        clock.tick(1)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_application()
