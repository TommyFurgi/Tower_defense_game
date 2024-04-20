from typing import Any
import pygame
from abc import ABC, abstractmethod


class Tower(pygame.sprite.Sprite, ABC): 
    
    def __init__(self, x, y): 

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.level = 1
        self.selected = False

        self.time_from_last_shot = pygame.time.get_ticks()
        

        
        
    def draw(self, screen):
        image = self.tower_imgs[self.level-1]

        if self.selected:
            self.draw_radius(screen)
            # TODO: draw menu for upgrade

    
        screen.blit(image, (self.x-image.get_width()//2, self.y-image.get_height()//2))


    def draw_radius(self, screen):
        scale_rate = 1.2

        surface = pygame.Surface((self.radius * 2 * scale_rate, self.radius * 2 * scale_rate), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 255, 100), (self.radius*scale_rate, self.radius*scale_rate), self.radius*scale_rate, 0)

        screen.blit(surface, (self.x - self.radius * scale_rate, self.y - self.radius * scale_rate))



    def click(self, X, Y):
        img = self.tower_imgs[self.level - 1]
        if abs(X-self.x) < img.get_width()//2:
            if abs(Y-self.y) < img.get_height()//2:
                self.selected = True
                
                return True
        return False
    
    
    
        
        
        