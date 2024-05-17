import pygame
from abc import ABC


class Tower(pygame.sprite.Sprite, ABC): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.level = 1
        self.selected = False

        self.time_from_last_shot = pygame.time.get_ticks()

        sell_icon = pygame.image.load('assets/towers/sell_icon.png').convert_alpha()
        self.sell_icon = pygame.transform.scale(sell_icon, (50, 50))

        upgrade_icon = pygame.image.load('assets/towers/upgraded_icon.png').convert_alpha()
        self.upgrade_icon = pygame.transform.scale(upgrade_icon, (50, 50))
        self.font = pygame.font.Font(None, 24) 
        

    def draw(self, screen):
        screen.blit(self.image, (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))


    def draw_tower_menu(self, screen):
        upgrade_rect = pygame.Rect(self.x + self.radius * 0.5, self.y + self.radius * 0.3 - 5, 150, 60)
        pygame.draw.ellipse(screen, (133, 98, 42), upgrade_rect)

        screen.blit(self.sell_icon, (self.x + self.radius * 0.5, self.y + self.radius * 0.3))

        text = self.font.render("Price: " + str(self.price), True, (255, 255, 255))
        screen.blit(text, (self.x + self.radius * 0.5 + 60, self.y + self.radius * 0.3 + 15))

        if self.level <= 3:
            upgrade_rect = pygame.Rect(self.x + self.radius * 0.5, self.y - self.radius * 0.3 - 5, 150, 60)
            pygame.draw.ellipse(screen, (133, 98, 42), upgrade_rect)

            screen.blit(self.upgrade_icon, (self.x + self.radius * 0.5, self.y - self.radius * 0.3))

            text = self.font.render("Price: " + str(self.price), True, (255, 255, 255))
            screen.blit(text, (self.x + self.radius * 0.5 + 60, self.y - self.radius * 0.3 + 10))

            level_text = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
            screen.blit(level_text, (self.x + self.radius * 0.5 + 60, self.y - self.radius * 0.3 + 30))


    def draw_on_top(self, screen):
        if self.selected:
            self.draw_radius(screen)
            self.draw(screen) # So the tower isn't drawn under the circle
            self.draw_tower_menu(screen)


    def manage_tower_action(self, clicked_position, money):
        if self.sell_icon_rect.collidepoint(clicked_position):
            return self.price

        if self.level <= 3 and self.upgrade_icon_rect.collidepoint(clicked_position):
            if money - self.price < 0:
                # TODO: inform about not enough money
                return 0
            
            self.level += 1
            self.damage *= 1.2
            self.radius *= 1.1
            self.cooldown *= 0.9

            self.update_tower_feature_rect()

            return -self.price
        
        return 0


    def update_tower_feature_rect(self):
        self.sell_icon_rect = pygame.Rect(self.x + self.radius * 0.5, self.y + self.radius * 0.3, 50, 50) 
        self.upgrade_icon_rect = pygame.Rect(self.x + self.radius * 0.5, self.y - self.radius * 0.3, 50, 50)  


    def draw_radius(self, screen):
        scale_rate = 1.3

        surface = pygame.Surface((self.radius * 2 * scale_rate, self.radius * 2 * scale_rate), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 255, 100), (self.radius*scale_rate, self.radius*scale_rate), self.radius*scale_rate, 0)

        screen.blit(surface, (self.x - self.radius * scale_rate, self.y - self.radius * scale_rate))


    def select_tower(self, X, Y):
        if abs(X-self.x) < self.image.get_width()//2:
            if abs(Y-self.y) < self.image.get_height()//2:
                self.selected = True
                
                return True
        return False
    