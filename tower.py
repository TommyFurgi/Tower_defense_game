import pygame
from abc import ABC, abstractmethod


# base class for towers
class Tower(pygame.sprite.Sprite, ABC): # ABC means Tower is abstrac class
    
    # player grabbed a tower from the menu
    def __init__(self, image): 

        pygame.sprite.Sprite.__init__(self)
    
        self.image = image
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = self.calcualte_position() # initial position, cant be None
    
    # makes sure tower is being held in the middle
    def calcualte_position(self):
        
        mouse_position = pygame.mouse.get_pos()
        return (mouse_position[0] - self.image.get_width() // 2, mouse_position[1] - self.image.get_height() // 2)

    # makes tower follow a mouse
    def move(self):
        
        self.rect.x, self.rect.y = self.calcualte_position()
    
    def place(self):
        
        # TODO:
        # check if position if valid
        # should check if its overlapping any forbidden areas (path, trees, rocks)
        
        self.move() #make sure tower is in desired position
        
        return True

    # each tower should define its behaviour
    @abstractmethod
    def update():
        pass
    
        
    
        
        
        