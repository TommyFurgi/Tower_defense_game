import pygame

class Tower(pygame.sprite.Sprite):
    
    def __init__(self, tower_image): # player grabbed a tower from the menu

        pygame.sprite.Sprite.__init__(self)
    
        self.image = tower_image
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = self.calcualte_position()
        
        #self.rect.center = (self.image.get_width() // 2, self.image.get_height() // 2)
    
    def calcualte_position(self):
        
        mouse_position = pygame.mouse.get_pos()
        return (mouse_position[0] - self.image.get_width() // 2, mouse_position[1] - self.image.get_height() // 2)

    
    def follow_mouse(self):
        
        self.rect.x, self.rect.y = self.calcualte_position()
    
    def place(self):
        
        #TODO: check if position if valid
        
        self.rect.x, self.rect.y = self.calcualte_position()
        
        return True

        
    
        
        
        