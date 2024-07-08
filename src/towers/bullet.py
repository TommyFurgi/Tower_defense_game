import pygame, math
from resource_manager import ResourceManager


class Bullet(pygame.sprite.Sprite):
    """
    Bullet is making its way from start to destination is n steps.
    It also seeks one specified enemy and implements a self.hit method
    to check if the enemy was reached.
    """
    def __init__(self, bullet_size, x_start, y_start, x_destination, y_destination, enemy, x_scale_rate, y_scale_rate): 
        pygame.sprite.Sprite.__init__(self)

        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.x = x_start  
        self.y = y_start  

        self.destination_x = x_destination  
        self.destination_y = y_destination
        self.enemy = enemy
        
        self.bullet_size = bullet_size
        self.speed = 10
        self.dirn = ((self.destination_x-self.x) * 2, (self.destination_y-self.y) * 2)
        self.length = math.sqrt((self.dirn[0])**2 + (self.dirn[1])**2)
        self.dirn = (self.dirn[0]/self.length, self.dirn[1]/self.length)
        self.dirn = (self.dirn[0] * self.speed, self.dirn[1] * self.speed)

        self.bullet = ResourceManager.get_image("bullet-01").convert_alpha()
        self.bullet_transformed = pygame.transform.scale(self.bullet, (bullet_size * x_scale_rate, bullet_size * y_scale_rate))
    

    def draw(self, screen):
        """Draws a bullet on a screen"""
        screen.blit(self.bullet_transformed, (self.x-self.bullet_transformed.get_width()//2, self.y-self.bullet_transformed.get_height()//2))


    def update(self, game_pause, screen):
        """
        Function called every frame, responsible for changing
        bullet's position (Moving it forward).
        """
        if not game_pause:
            self.x, self.y = ((self.x + self.dirn[0]), (self.y + self.dirn[1]))

        self.draw(screen)


    def hit(self):
        """Function checks if enemy was hit."""
        if self.dirn[0] >= 0: # moving right
            if self.dirn[1] >= 0: # moving down
                if self.x >= self.destination_x and self.y >= self.destination_y:
                    return self.enemy
            else:
                if self.x >= self.destination_x and self.y <= self.destination_y:
                    return self.enemy
        else: # moving left
            if self.dirn[1] >= 0:  # moving down
                if self.x <= self.destination_x and self.y >= self.destination_y:
                    return self.enemy
            else:
                if self.x <= self.destination_x and self.y <= self.destination_y:
                    return self.enemy
        
        return None
    
    
    def scale_parameters(self, x_scale_rate, y_scale_rate):
        """
        Scales necessary parameters. Triggered when users
        resizes game window.
        """
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate
        
        self.bullet_transformed = pygame.transform.scale(self.bullet, (self.bullet_size * x_scale_rate, self.bullet_size * x_scale_rate))