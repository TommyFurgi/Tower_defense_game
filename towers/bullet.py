import pygame, math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_start, y_start, x_destination, y_destination, enemy): 
        pygame.sprite.Sprite.__init__(self)

        self.x = x_start  
        self.y = y_start  

        self.destination_x = x_destination  
        self.destination_y = y_destination
        self.enemy = enemy
        
        self.speed = 10
        self.dirn = ((self.destination_x-self.x) * 2, (self.destination_y-self.y) * 2)
        self.length = math.sqrt((self.dirn[0])**2 + (self.dirn[1])**2)
        self.dirn = (self.dirn[0]/self.length, self.dirn[1]/self.length)
        self.dirn = (self.dirn[0] * self.speed, self.dirn[1] * self.speed)

        self.bullet = pygame.image.load('img/bullet-01.png')
        self.bullet = pygame.transform.scale(self.bullet, (15, 15))
    
    def draw(self, screen):
        screen.blit(self.bullet, (self.x-self.bullet.get_width()//2, self.y-self.bullet.get_height()//2))

    def update(self, game_pause, screen):
        if not game_pause:
            self.x, self.y = ((self.x + self.dirn[0]), (self.y + self.dirn[1]))

        self.draw(screen)


    def hit(self):
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