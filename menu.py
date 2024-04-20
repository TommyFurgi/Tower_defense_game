import pygame
from towers.tower import Tower

class Menu():
    def __init__(self, screen):
        self.screen = screen
        
        self.window_width, self.height = screen.get_size()
        self.width = 0.15 * self.window_width # 247.5
        self.left_border = self.window_width - self.width # 1402.5

        self.scale_rate = self.height / self.width # 3.63
        
        self.font = pygame.font.Font(None, int(10 * self.scale_rate))
        self.background_color = (214, 189, 120)
        self.rect = pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        
        self.hearth = pygame.image.load('img/heart.png')
        self.hearth = pygame.transform.scale(self.hearth, (15 * self.scale_rate, 15 * self.scale_rate))
        
        self.archer = pygame.image.load('img/archer_tower.png')
        self.archer = pygame.transform.scale(self.archer, (41 * self.scale_rate, 41 * self.scale_rate))

        self.play = pygame.image.load('img/play_button.png')
        self.play = pygame.transform.scale(self.play, (60, 60))

        self.stop = pygame.image.load('img/stop_button.png')
        self.stop = pygame.transform.scale(self.stop, (60, 60))

    def draw_all_menu(self, points, money, hearts):
        pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        self.draw_points(points)
        self.draw_hearts(hearts)
        self.draw_money(money)

        self.play_rect = self.screen.blit(self.play, (1410, 820))
        self.stop_rect = self.screen.blit(self.stop, (1480, 820))
        
        self.archer_tower_rect = self.screen.blit(self.archer, (self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2, self.height * 0.3))

    def draw_points(self, points):
        score = self.font.render(f'Score: {points}', True, (0, 0, 0))
        self.screen.blit(score, (self.left_border + self.width * 0.1, 0.02 * self.height))

    def draw_hearts(self, health_points):
        if (health_points > 0):
            self.screen.blit(self.hearth, (self.left_border + self.width * 0.25 - 7.5 * self.scale_rate, self.height * 0.2))

        if (health_points > 1):
            self.screen.blit(self.hearth, (self.left_border + self.width * 0.5 - 7.5 * self.scale_rate, self.height * 0.2))

        if (health_points > 2):
            self.screen.blit(self.hearth, (self.left_border + self.width * 0.75 - 7.5 * self.scale_rate, self.height * 0.2))
    
    def draw_money(self, money):
        money = self.font.render(f'Money: {money}', True, (0, 0, 0))
        self.screen.blit(money, (self.left_border + self.width * 0.1, self.height * 0.1))        


    def handle_click(self, clicked_position):
        if (self.archer_tower_rect.collidepoint(clicked_position)):
            return self.archer, "archer"
        
        if (self.play_rect.collidepoint(clicked_position)):
            return None, "play"
        
        if (self.stop_rect.collidepoint(clicked_position)):
            return None, "stop"
        
        return None, None

        
