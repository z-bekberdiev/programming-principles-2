import pygame
import math


class Paint:
    def __init__(self):
        pygame.init()

        # Create main window
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Paint")

        clock = pygame.time.Clock()
        font = pygame.font.SysFont("SF Mono", 15)

        position = (0, 0)  # Starting mouse position
        rectangle = pygame.Rect(0, 0, 0, 0)  # Current drawing rectangle

        # Left-side menu area
        menu = pygame.Rect(10, 10, 245, 470)

        # Drawing area (everything except menu)
        area = pygame.Rect(
            menu.right + 10,
            10,
            screen.get_width() - (menu.right + 10) - 10,
            screen.get_height() - 20
        )

        # Default drawing settings
        figure = "circle"
        color = (255, 0, 0)
        thickness = 2

        shapes = []  # Stores all finalized shapes

        # Menu text
        choices = [
            "Draw a figure:",
            "1 - Circle",
            "2 - Square",
            "3 - Rectangle",
            "4 - Right Triangle",
            "5 - Equilateral Triangle",
            "6 - Rhombus",
            "7 - Eraser",
            "Choose a color:",
            "R - Red",
            "G - Green",
            "B - Blue",
            "Resize a figure:",
            "I - Increase",
            "D - Decrease"
        ]

        running = True
        drawing = False  # True while mouse is held down

        while running:
            screen.fill((255, 255, 255))

            # Draw menu outline
            pygame.draw.rect(screen, (0, 0, 0), menu, 2)

            # Render menu text
            for index, choice in enumerate(choices):
                if index in [0, 8, 12]:  # Section headers
                    font.bold = True

                text = font.render(choice, True, (0, 0, 0))
                screen.blit(text, (25, 25 + index * 30))
                font.bold = False

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Exit shortcut
                    if event.key == pygame.K_q:
                        running = False

                    # Shape selection
                    if event.key == pygame.K_1:
                        figure = "circle"
                    if event.key == pygame.K_2:
                        figure = "square"
                    if event.key == pygame.K_3:
                        figure = "rectangle"
                    if event.key == pygame.K_4:
                        figure = "right triangle"
                    if event.key == pygame.K_5:
                        figure = "equilateral triangle"
                    if event.key == pygame.K_6:
                        figure = "rhombus"
                    if event.key == pygame.K_7:
                        figure = "eraser"

                    # Color selection
                    if event.key == pygame.K_r:
                        color = (255, 0, 0)
                    if event.key == pygame.K_g:
                        color = (0, 255, 0)
                    if event.key == pygame.K_b:
                        color = (0, 0, 255)

                    # Thickness control (clamped between 1 and 8)
                    if event.key == pygame.K_i:
                        thickness = min(8, thickness + 1)
                    if event.key == pygame.K_d:
                        thickness = max(1, thickness - 1)

                # Start drawing only if inside drawing area
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if area.collidepoint(event.pos):
                        drawing = True
                        position = event.pos

                # Update shape preview while dragging mouse
                if event.type == pygame.MOUSEMOTION and drawing:
                    mx, my = event.pos

                    # Keep mouse inside drawing area
                    mx = max(area.left, min(mx, area.right))
                    my = max(area.top, min(my, area.bottom))

                    width = mx - position[0]
                    height = my - position[1]

                    rectangle = pygame.Rect(position, (width, height))
                    rectangle.normalize()  # Fix negative width/height

                    # Ensure rectangle stays inside drawing area
                    rectangle.clamp_ip(area)

                # Finalize shape when mouse released
                if event.type == pygame.MOUSEBUTTONUP:
                    if drawing:
                        drawing = False
                        temp = rectangle.copy()

                        # Save only if fully inside drawing area
                        if area.contains(temp):
                            shapes.append((figure, temp, color, thickness))

            # Draw all saved shapes
            for fig, rect, col, thick in shapes:
                self.draw(screen, fig, rect, col, thick)

            # Draw current preview shape
            if drawing:
                self.draw(screen, figure, rectangle, color, thickness)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw(self, screen, figure, rectangle, color, thickness):
        # Draw shapes based on selected type
        if figure == "rectangle":
            pygame.draw.rect(screen, color, rectangle, thickness)

        elif figure == "square":
            # Force equal width and height
            size = min(rectangle.width, rectangle.height)
            square = pygame.Rect(rectangle.x, rectangle.y, size, size)
            pygame.draw.rect(screen, color, square, thickness)

        elif figure == "circle":
            # Fit circle inside bounding rectangle
            radius = min(rectangle.width, rectangle.height) // 2
            center = rectangle.center
            pygame.draw.circle(screen, color, center, radius, thickness)

        elif figure == "right triangle":
            # Triangle using three rectangle corners
            points = [
                rectangle.topleft,
                rectangle.bottomleft,
                rectangle.bottomright
            ]
            pygame.draw.polygon(screen, color, points, thickness)

        elif figure == "equilateral triangle":
            # Calculate proper triangle height using geometry
            x, y, w, h = rectangle

            side = abs(w)
            height = side * math.sqrt(3) / 2

            if h < 0:
                height = -height

            points = [
                (x + side / 2, y),
                (x, y + height),
                (x + side, y + height)
            ]

            pygame.draw.polygon(screen, color, points, thickness)

        elif figure == "rhombus":
            # Diamond shape centered in rectangle
            x, y, w, h = rectangle
            points = [
                (x + w // 2, y),
                (x + w, y + h // 2),
                (x + w // 2, y + h),
                (x, y + h // 2)
            ]
            pygame.draw.polygon(screen, color, points, thickness)

        elif figure == "eraser":
            # Draw white rectangle to erase
            pygame.draw.rect(screen, (255, 255, 255), rectangle)


def execute():
    Paint()


if __name__ == "__main__":
    execute()