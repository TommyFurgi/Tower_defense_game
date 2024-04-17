import pygame
from towers.tower import Tower
from menu import Menu

class ArcherTower(Tower):

    def __init__(self, x, y, screen):
        
        Tower.__init__(self, x, y)

        image = pygame.image.load('img/archer_tower.png')
        image = pygame.transform.scale(image, (150, 150))
        
        # This two attributes are required by pygame.sprite.Sprite in order for it to work properly
        self.image = image
        self.rect = pygame.Rect(x, y, 50, 50) # Rect(left, top, width, height), but we want x,y to be the center of the tower
        self.rect.center = (x, y) # thus this line is needed
        
        self.tower_imgs = [image]


    def update(self):
        
        #self.find_targets()
        
        pass

        
    
        
        
        