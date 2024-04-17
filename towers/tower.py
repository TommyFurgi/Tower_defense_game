import pygame
from abc import ABC, abstractmethod


class Tower(pygame.sprite.Sprite, ABC): 
    
    def __init__(self, x, y): 

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.level = 1
        self.selected = False

        self.tower_imgs = []
        self.damage = 1
        self.range = 150
        
        self.radius = self.range
        
    def draw(self, screen):
        image = self.tower_imgs[self.level-1]

        if self.selected:
            self.draw_radius(screen)
            # TODO: draw menu for upgrade

    
        screen.blit(image, (self.x-image.get_width()//2, self.y-image.get_height()//2))


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
    
    def find_targets(self, enemies):
        
        # True znaczy, że obiekty, które wejdą w kolizję z okręgie dookoła wieży są usuwane
        # TODO: zmienić True na False i zamiast tego dodać zadawanie obrażeń
        enemies_collision = pygame.sprite.spritecollide(self, enemies, True, pygame.sprite.collide_circle)
        
        return enemies_collision
    
        
    
        
        
        