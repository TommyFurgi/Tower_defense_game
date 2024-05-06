import pygame
from towers.tower import Tower

class Menu():
    def __init__(self, screen):
        self.screen = screen
        
        self.window_width, self.height = screen.get_size()
        self.width = 0.15 * self.window_width
        self.left_border = self.window_width - self.width # 1402.5
        
        self.scale_rate = self.height / self.width # 3.63
        
        self.font = pygame.font.Font(None, int(50))
        self.background_color = (214, 189, 120)
        self.rect = pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        
        self.points = pygame.image.load('assets/menu/points.png')
        self.points = pygame.transform.scale(self.points, (10* self.scale_rate, 10 * self.scale_rate))

        self.money = pygame.image.load('assets/menu/resources.png')
        self.money = pygame.transform.scale(self.money, (10 * self.scale_rate, 10 * self.scale_rate))

        self.wave = pygame.image.load('assets/menu/wave.png')
        self.wave = pygame.transform.scale(self.wave, (10 * self.scale_rate, 10 * self.scale_rate))

        self.hearth = pygame.image.load('assets/menu/lives.png')
        self.hearth = pygame.transform.scale(self.hearth, (20 * self.scale_rate, 20 * self.scale_rate))
        
        self.archer = pygame.image.load('assets/towers/archer_tower.png')
        self.archer = pygame.transform.scale(self.archer, (41 * self.scale_rate, 41 * self.scale_rate))
        self.archer_price = 400

        # Consider using tuple as one object atribute 
        self.magic = pygame.image.load('assets/towers/magic_tower.png')
        self.magic = pygame.transform.scale(self.magic, (41 * self.scale_rate, 41 * self.scale_rate))
        self.magic_price = 300

        self.play = pygame.image.load('assets/menu/play_button.png')
        self.play = pygame.transform.scale(self.play, (60, 60))

        self.stop = pygame.image.load('assets/menu/stop_button.png')
        self.stop = pygame.transform.scale(self.stop, (60, 60))

        self.music = pygame.image.load('assets/menu/music.png')
        self.music = pygame.transform.scale(self.music, (60, 60))
        
        self.scroll_up = pygame.image.load('assets/menu/play_button.png')
        self.scroll_up = pygame.transform.rotate(self.scroll_up, 90)
        self.scroll_up = pygame.transform.scale(self.scroll_up, (30, 30))
        
        self.scroll_down = pygame.image.load('assets/menu/play_button.png')
        self.scroll_down = pygame.transform.rotate(self.scroll_down, 270)
        self.scroll_down = pygame.transform.scale(self.scroll_down, (30, 30))
        
        self.displayed_towers = []
        

    def draw_all_menu(self, points, money, hearts, wave):
        pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        self.draw_points(points)
        self.draw_hearts(hearts)
        self.draw_money(money)
        self.draw_wave_counter(wave)

        self.play_rect = self.screen.blit(self.play, (1380, 820))
        self.stop_rect = self.screen.blit(self.stop, (1450, 820))
        self.music_rect = self.screen.blit(self.music, (1520, 820))
        
        self.scroll_up_rect = self.screen.blit(self.scroll_up, (1465, 245))
        self.scroll_down_rect = self.screen.blit(self.scroll_down, (1465, 765))
        
        
        self.draw_towers_shop()

    def draw_towers_shop(self):
        ar_price = self.font.render(f'{self.archer_price}', True, (0, 0, 0))
        self.screen.blit(self.money, (self.left_border + self.width * 0.35 - 10 * self.scale_rate,  self.height * 0.52))
        self.screen.blit(ar_price, (self.left_border + self.width * 0.4, self.height * 0.52)) 
        self.archer_tower_rect = self.screen.blit(self.archer, (self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2, self.height * 0.32))


        ma_price = self.font.render(f'{self.magic_price}', True, (0, 0, 0))
        self.screen.blit(self.money, (self.left_border + self.width * 0.35 - 10 * self.scale_rate,  self.height * 0.8))
        self.screen.blit(ma_price, (self.left_border + self.width * 0.4, self.height * 0.8)) 
        self.magic_tower_rect = self.screen.blit(self.magic, (self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2, self.height * 0.6))


    def draw_points(self, points):
        score = self.font.render(f'{points}', True, (0, 0, 0))
        self.screen.blit(self.points, (self.left_border + self.width * 0.2 - 10 * self.scale_rate, self.height * 0.16))
        self.screen.blit(score, (self.left_border + self.width * 0.3, self.height * 0.16))

    def draw_hearts(self, health_points):
        if (health_points > 0):
            self.screen.blit(self.hearth, (self.left_border + self.width * 0.2 - 10 * self.scale_rate, self.height * 0.01))

        if (health_points > 1):
            self.screen.blit(self.hearth, (self.left_border + self.width * 0.5 - 10 * self.scale_rate, self.height * 0.01))

        if (health_points > 2):
            self.screen.blit(self.hearth, (self.left_border + self.width * 0.8 - 10 * self.scale_rate, self.height * 0.01))
    
    def draw_money(self, money):
        money = self.font.render(f'{money}', True, (0, 0, 0))
        self.screen.blit(self.money, (self.left_border + self.width * 0.2 - 10 * self.scale_rate,  self.height * 0.21))
        self.screen.blit(money, (self.left_border + self.width * 0.3, self.height * 0.21))        

    def draw_wave_counter(self, wave):
        wave = self.font.render(f'{wave}', True, (0, 0, 0))
        self.screen.blit(self.wave, (self.left_border + self.width * 0.2 - 10 * self.scale_rate,  self.height * 0.11))
        self.screen.blit(wave, (self.left_border + self.width * 0.3, self.height * 0.11))        


    def handle_click(self, clicked_position):
        if (self.archer_tower_rect.collidepoint(clicked_position)):
            return self.archer, "archer", self.archer_price
        
        if (self.magic_tower_rect.collidepoint(clicked_position)):
            return self.magic, "magic", self.magic_price
        
        if (self.play_rect.collidepoint(clicked_position)):
            return None, "play", 0
        
        if (self.stop_rect.collidepoint(clicked_position)):
            return None, "stop", 0
        
        if (self.music_rect.collidepoint(clicked_position)):
            return None, "music", 0
        
        if(self.scroll_up_rect.collidepoint(clicked_position)):
            #TODO: scroll up
            pass
        
        if(self.scroll_down_rect.collidepoint(clicked_position)):
            #TODO: scroll down
            pass
        
            

        
        return None, None, 0

        
