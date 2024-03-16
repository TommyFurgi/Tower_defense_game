import pygame
from pygame.locals import *
 
class Back_ground(pygame.sprite.Sprite):
    
    def __init__(self, image_file, screen):
        pygame.sprite.Sprite.__init__(self)  
        self.screen = screen
        window_width, self.height = screen.get_size()
        self.width = 0.85 * window_width
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]


    