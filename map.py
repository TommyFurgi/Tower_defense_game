import pygame
from source_manager import SourceManager
 
 
class Map():
    def __init__(self, screen):
        self.screen = screen
        
        window_width, self.height = screen.get_size()
        self.width = 0.85 * window_width 

        self.background = SourceManager.get_image("map").convert()
        self.background_transformated = pygame.transform.scale(self.background, (self.width, self.height))


    def draw_background(self):
        self.screen.blit(self.background_transformated, (0, 0))
       

    def scale_parameters(self, x_scale_rate, y_scale_rate):
        self.background_transformated = pygame.transform.scale(self.background, (self.width * x_scale_rate, self.height * y_scale_rate))