import pygame
import pathlib
import datetime
from tools import draw_shape, flood_fill

class Paint:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Paint")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("SF Mono", 15)

        # Menu and drawing area
        self.menu = pygame.Rect(10, 10, 245, 600)
        self.area = pygame.Rect(self.menu.right + 10, 10,
                                self.screen.get_width() - (self.menu.right + 20),
                                self.screen.get_height() - 20)

        # Canvas surface (everything drawn by user)
        self.canvas = pygame.Surface((self.area.width, self.area.height))
        self.canvas.fill((255, 255, 255))  # white background

        # Defaults
        self.figure = "circle"
        self.color = (255, 0, 0)
        self.thickness = 2
        self.shapes = []  # For replay and preview
        self.drawing = False
        self.prev_pos = None
        self.text_buffer = ""
        self.typing = False
        self.text_pos = (0, 0)

        self.run()

    def run(self):
        while True:
            self.screen.fill((200, 200, 200))  # background
            self.draw_menu()
            self.screen.blit(self.canvas, (self.area.left, self.area.top))  # show canvas
            self.handle_events()
            self.draw_shapes()  # for preview and text typing
            pygame.display.flip()
            self.clock.tick(60)

    def draw_menu(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.menu, 2)
        choices = [
            "Tools:", "P - Pencil", "L - Line", "T - Text", "F - Fill",
            "Draw:", "0 - Circle", "1 - Square", "2 - Rectangle",
            "3 - Right Triangle", "4 - Equilateral Triangle", "5 - Rhombus",
            "6 - Eraser",
            "Colors:", "R - Red", "G - Green", "B - Blue",
            "Thickness:", "7 - Small", "8 - Medium", "9 - Large",
            "Ctrl+S - Save", "Q - Quit"
        ]
        for idx, text in enumerate(choices):
            txt_surf = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(txt_surf, (25, 25 + idx * 25))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_RETURN:
                        font = pygame.font.SysFont("SF Mono", 20)
                        # Render text with white background
                        txt_surface = font.render(self.text_buffer, True, self.color, (255, 255, 255))
                        self.canvas.blit(txt_surface, self.text_pos)
                        self.typing = False
                        self.text_buffer = ""
                    elif event.key == pygame.K_ESCAPE:
                        self.typing = False
                        self.text_buffer = ""
                    else:
                        self.text_buffer += event.unicode
                    continue

                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    pygame.image.save(self.canvas, f"{pathlib.Path(__file__).parent}/assets/canvas_{timestamp}.png")

                # Tools
                if event.key == pygame.K_p: self.figure = "pencil"
                if event.key == pygame.K_l: self.figure = "line"
                if event.key == pygame.K_t: self.figure = "text"
                if event.key == pygame.K_f: self.figure = "fill"

                # Shapes
                if event.key == pygame.K_0: self.figure = "circle"
                if event.key == pygame.K_1: self.figure = "square"
                if event.key == pygame.K_2: self.figure = "rectangle"
                if event.key == pygame.K_3: self.figure = "right triangle"
                if event.key == pygame.K_4: self.figure = "equilateral triangle"
                if event.key == pygame.K_5: self.figure = "rhombus"
                if event.key == pygame.K_6: self.figure = "eraser"

                # Colors
                if event.key == pygame.K_r: self.color = (255, 0, 0)
                if event.key == pygame.K_g: self.color = (0, 255, 0)
                if event.key == pygame.K_b: self.color = (0, 0, 255)

                # Thickness
                if event.key == pygame.K_7: self.thickness = 2
                if event.key == pygame.K_8: self.thickness = 5
                if event.key == pygame.K_9: self.thickness = 10

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.area.collidepoint(event.pos):
                    x, y = event.pos
                    canvas_pos = (x - self.area.left, y - self.area.top)
                    if self.figure == "fill":
                        flood_fill(self.canvas, *canvas_pos, self.color)
                    elif self.figure == "text":
                        self.typing = True
                        self.text_pos = canvas_pos
                        self.text_buffer = ""
                    else:
                        self.drawing = True
                        self.start_pos = canvas_pos
                        if self.figure == "pencil":
                            self.prev_pos = canvas_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing:
                    x, y = event.pos
                    end_pos = (x - self.area.left, y - self.area.top)
                    if self.figure == "line":
                        draw_shape(self.canvas, "line", (self.start_pos, end_pos), self.color, self.thickness)
                    elif self.figure != "pencil":
                        rect = pygame.Rect(self.start_pos, (end_pos[0]-self.start_pos[0], end_pos[1]-self.start_pos[1]))
                        rect.normalize()
                        draw_shape(self.canvas, self.figure, rect, self.color, self.thickness)
                    self.drawing = False
                    self.prev_pos = None

            if event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    x, y = event.pos
                    pos = (x - self.area.left, y - self.area.top)
                    if self.figure == "pencil":
                        pygame.draw.line(self.canvas, self.color, self.prev_pos, pos, self.thickness)
                        self.prev_pos = pos

    def draw_shapes(self):
        # Draw preview shapes on top of canvas
        if self.drawing and self.figure not in ["pencil", "line"]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            canvas_mouse = (mouse_x - self.area.left, mouse_y - self.area.top)
            rect = pygame.Rect(self.start_pos, (canvas_mouse[0]-self.start_pos[0], canvas_mouse[1]-self.start_pos[1]))
            rect.normalize()
            draw_shape(self.screen, self.figure, rect, self.color, self.thickness)

        if self.drawing and self.figure == "line":
            mouse_x, mouse_y = pygame.mouse.get_pos()
            canvas_mouse = (mouse_x - self.area.left, mouse_y - self.area.top)
            draw_shape(self.screen, "line", (self.start_pos, canvas_mouse), self.color, self.thickness)

        # Draw text while typing
        if self.typing:
            txt_surface = self.font.render(self.text_buffer, True, self.color)
            self.screen.blit(txt_surface, (self.text_pos[0] + self.area.left, self.text_pos[1] + self.area.top))


def execute():
    Paint()


if __name__ == "__main__":
    execute()