import pygame
import math
from collections import deque

def draw_shape(screen, figure, rectangle, color, thickness):
    """Draws a shape based on the figure type"""
    if figure == "rectangle":
        pygame.draw.rect(screen, color, rectangle, thickness)
    elif figure == "square":
        size = min(rectangle.width, rectangle.height)
        square = pygame.Rect(rectangle.x, rectangle.y, size, size)
        pygame.draw.rect(screen, color, square, thickness)
    elif figure == "circle":
        radius = min(rectangle.width, rectangle.height) // 2
        center = rectangle.center
        pygame.draw.circle(screen, color, center, radius, thickness)
    elif figure == "right triangle":
        points = [rectangle.topleft, rectangle.bottomleft, rectangle.bottomright]
        pygame.draw.polygon(screen, color, points, thickness)
    elif figure == "equilateral triangle":
        x, y, w, h = rectangle
        side = abs(w)
        height = side * math.sqrt(3) / 2
        if h < 0:
            height = -height
        points = [(x + side / 2, y), (x, y + height), (x + side, y + height)]
        pygame.draw.polygon(screen, color, points, thickness)
    elif figure == "rhombus":
        x, y, w, h = rectangle
        points = [(x + w // 2, y), (x + w, y + h // 2),
                  (x + w // 2, y + h), (x, y + h // 2)]
        pygame.draw.polygon(screen, color, points, thickness)
    elif figure == "eraser":
        pygame.draw.rect(screen, (255, 255, 255), rectangle, 0)
    elif figure == "line":
        start, end = rectangle
        pygame.draw.line(screen, color, start, end, thickness)
    elif figure == "text":
        text, pos, font = rectangle  # rectangle stores (text, pos, font)
        txt_surface = font.render(text, True, color, (255, 255, 255))
        screen.blit(txt_surface, pos)

def flood_fill(surface, x, y, fill_color):
    """Flood fill algorithm using a stack (iterative)"""
    target_color = surface.get_at((x, y))
    if target_color == fill_color:
        return
    stack = deque([(x, y)])
    while stack:
        px, py = stack.pop()
        if surface.get_at((px, py)) != target_color:
            continue
        surface.set_at((px, py), fill_color)
        if px > 0: stack.append((px-1, py))
        if px < surface.get_width() - 1: stack.append((px+1, py))
        if py > 0: stack.append((px, py-1))
        if py < surface.get_height() - 1: stack.append((px, py+1))