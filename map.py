import pygame
 
class Map():
    def __init__(self, screen):
        self.screen = screen
        
        window_width, self.height = screen.get_size()
        self.width = 0.85 * window_width 

        self.background = pygame.image.load("img/map.jpg")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.draw_background()

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        
        


    