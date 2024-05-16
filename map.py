import pygame
 
class Map():
    def __init__(self, screen):
        self.screen = screen
        
        window_width, self.height = screen.get_size()
        self.width = 0.85 * window_width 

        self.background = pygame.image.load("assets/map.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.draw_background()

        self.font_buttons = pygame.font.Font(None, 24) 
        self.font_game_status = pygame.font.Font(None, 128)
        self.button_color = (83, 142, 237, 50)

        self.return_to_menu_rect = pygame.Rect(0, 0, 0, 0)
        self.restart_game_rect = pygame.Rect(0, 0, 0, 0)


    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        