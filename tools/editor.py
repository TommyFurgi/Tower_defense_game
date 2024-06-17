import pygame
import sys

class Editor():
    """
    Editor's purpose is drawing rectangles on screen, which are being used to
    determine collistions with environment objects (since they are not seperate
    objects,but rather one image)

    How to implement it:
    1) Import Editor class
    2) Initnialize Editor class with screen variable and filename
    3) Call edit() in main game loop 
    4) pygame.display.flip() must be called after edit()

    How to use it:
    1) Click left mouse button to create a rectangle
    2) Click right mouse button to delete a rectangle
    3) Click s to save rectangles to text file
    4) Click l to load rectangles from file (discards newly created rectangles unless saved)

    *) Init function loads rectangles from file with given filename

    """
    def __init__(self, screen, filename = "environment/rectangles.txt"):
        self.screen = screen
        self.filename = filename
        
        self.rectangles = []  # List to store rectangles
        self.drawing = False
        self.font = pygame.font.Font(None, 32)
        
        self.load_rectangles_from_file() # loading all existing rectangles from file


    def save_rectangles_to_file(self):
        """Saves all rectangles on screen to file"""
        with open(self.filename, "w") as file:
            for rectangle in self.rectangles:
                file.write(f"{rectangle[0]} {rectangle[1]} {rectangle[2]} {rectangle[3]}\n")


    def load_rectangles_from_file(self):
        """Loads all rectangles from file with given filename"""
        try:
            with open(self.filename, "r") as file:
                self.rectangles = []
                for line in file:
                    rect_x, rect_y, rect_width, rect_height = map(int, line.strip().split())
                    self.rectangles.append((rect_x, rect_y, rect_width, rect_height))
        except FileNotFoundError:
            print(f"File '{self.filename}' not found. No rectangles loaded.")


    def draw_rectangles(self):
        """Draws all rectangles from self.rectangles"""
        for rectangles in self.rectangles:
            rect_surface = pygame.Surface((rectangles[2], rectangles[3]), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (rectangles[0], rectangles[1]))


    def display_mouse_button_actions(self):
        """Displays info about keymap in edit mode"""
        # Render text for left mouse button action
        edit_mode_text = self.font.render("EDIT MODE", True, (255, 0, 0))
        # Render text for left mouse button action
        left_text = self.font.render("Left Click: Draw Rectangle", True, (255, 0, 0))
        # Render text for right mouse button action
        right_text = self.font.render("Right Click: Remove Rectangle", True, (255, 0, 0))
        # Render text for saving rectangles
        save_text = self.font.render("Press 'S' to Save Rectangles", True, (255, 0, 0))
        # Render text for loading rectangles
        load_text = self.font.render("Press 'L' to Load Rectangles", True, (255, 0, 0))

        # Calculate the dimensions of the black rectangle
        max_text_width = max(edit_mode_text.get_width(), left_text.get_width(), right_text.get_width(), save_text.get_width(), load_text.get_width())
        total_text_height = edit_mode_text.get_height() + left_text.get_height() + right_text.get_height() + save_text.get_height() + load_text.get_height()
        padding = 10  # Padding around the text

        # Calculate the position and size of the black rectangle
        rect_x = 10
        rect_y = 10
        rect_width = max_text_width + 2 * padding
        rect_height = total_text_height + 2 * padding

        # Render and fill the black rectangle
        black_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(self.screen, (0, 0, 0), black_rect)

        # Blit text onto the screen
        self.screen.blit(edit_mode_text, (rect_x + padding, rect_y + padding))
        self.screen.blit(left_text, (rect_x + padding, rect_y + padding + edit_mode_text.get_height()))
        self.screen.blit(right_text, (rect_x + padding, rect_y + padding + edit_mode_text.get_height() + left_text.get_height()))
        self.screen.blit(save_text, (rect_x + padding, rect_y + padding + edit_mode_text.get_height() + left_text.get_height() + right_text.get_height()))
        self.screen.blit(load_text, (rect_x + padding, rect_y + padding + edit_mode_text.get_height() + left_text.get_height() + right_text.get_height() + save_text.get_height()))


    def edit(self):
        """Function that handles all passible rectangle manipulation"""
        self.display_mouse_button_actions()
        self.draw_rectangles()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save_rectangles_to_file()
                elif event.key == pygame.K_l:
                    self.load_rectangles_from_file()
                    self.draw_rectangles()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if not self.drawing:
                        self.start_point = event.pos
                        self.drawing = True
                    else:
                        end_point = event.pos
                        self.drawing = False
                        rect_x = min(self.start_point[0], end_point[0])
                        rect_y = min(self.start_point[1], end_point[1])
                        rect_width = abs(end_point[0] - self.start_point[0])
                        rect_height = abs(end_point[1] - self.start_point[1])
                        self.rectangles.append((rect_x, rect_y, rect_width, rect_height))
                elif event.button == 3:  # Right mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect_props in enumerate(self.rectangles):
                        rect = pygame.Rect(rect_props)
                        if rect.collidepoint(mouse_pos):
                            del self.rectangles[i]
                            break
                        
        # Dynamically resizing rectangle
        if self.drawing:
            end_point = pygame.mouse.get_pos()

            rect_surface = pygame.Surface((abs(end_point[0] - self.start_point[0]),
                                           abs(end_point[1] - self.start_point[1])),
                                           pygame.SRCALPHA)
            transparent_red = (255, 0, 0, 128)
            pygame.draw.rect(rect_surface, transparent_red, rect_surface.get_rect())

            self.screen.blit(rect_surface, (min(self.start_point[0], end_point[0]),
                                            min(self.start_point[1], end_point[1])))
            pygame.display.flip()