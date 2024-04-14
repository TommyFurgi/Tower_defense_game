import pygame
from towers.tower import Tower
from menu import Menu

class ArcherTower(Tower):

    def __init__(self, x, y):
        Tower.__init__(self, x, y)

        image = pygame.image.load('img/archer_tower.png')
        image = pygame.transform.scale(image, (150, 150))
        self.tower_imgs = [image]


    def update(self):
        
        #self.find_targets()
        
        pass
    
    def find_targets(self):
        
        # TODO: create circular surface and check if it overlapps enemies
        
        pass


        
    
        
        
        