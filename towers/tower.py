import pygame
from abc import ABC, abstractmethod


class Tower(pygame.sprite.Sprite, ABC): 
    
    def __init__(self, x, y, screen): 

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.level = 1
        self.selected = False

        self.tower_imgs = []
        self.damage = 1
        self.range = 150
        self.screen = screen
    

    def draw(self):
        image = self.tower_imgs[self.level-1]

        if self.selected:
            self.draw_radius(self.screen)
            ... # TODO: draw menu for upgrade

        self.screen.blit(image, (self.x-image.get_width()//2, self.y-image.get_height()//2))


    def draw_radius(self, screen):
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 255, 100), (self.range, self.range), self.range, 0)

        screen.blit(surface, (self.x - self.range, self.y - self.range))



    def click(self, X, Y):
        img = self.tower_imgs[self.level - 1]
        if abs(X-self.x) < img.get_width()//2:
            if abs(Y-self.y) < img.get_height()//2:
                self.selected = True
                
                return True
        return False
    
    # def calcualte_position(self):
        
    #     mouse_position = pygame.mouse.get_pos()
    #     return (mouse_position[0] - self.image.get_width() // 2, mouse_position[1] - self.image.get_height() // 2)


    # def move(self):
        
    #     self.rect.x, self.rect.y = self.calcualte_position()
    
    # def place(self):
        
    #     # TODO:
    #     # check if position if valid
    #     # should check if its overlapping any forbidden areas (path, trees, rocks)
        
    #     self.move() #make sure tower is in desired position
        
    #     return True

    # # each tower should define its behaviour
    # @abstractmethod
    # def update():
    #     pass
    
        
    
        
        
        