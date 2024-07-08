import pygame
from resource_manager import ResourceManager
 
class Map():
    def __init__(self, screen):
        '''
        Initialize the Map object.

        Args:
            screen (pygame.Surface): The pygame screen surface object.
        '''
        self.screen = screen
        
        window_width, self.height = screen.get_size()
        self.width = 0.85 * window_width 

        self.background = ResourceManager.get_image("map").convert()
        self.background_transformated = pygame.transform.scale(self.background, (int(self.width), self.height))

    def draw_background(self):
        '''
        Draw the background image on the screen.
        '''
        self.screen.blit(self.background_transformated, (0, 0))
       
    def scale_parameters(self, x_scale_rate, y_scale_rate):
        '''
        Scale the background image based on the given scaling rates.

        Args:
            x_scale_rate (float): Scaling factor for the x-axis.
            y_scale_rate (float): Scaling factor for the y-axis.
        '''
        self.background_transformated = pygame.transform.scale(self.background, (int(self.width * x_scale_rate), int(self.height * y_scale_rate)))
