import pygame
from towers.tower import Tower

class Menu():
    def __init__(self, screen):
        self.screen = screen
        
        self.window_width, self.height = screen.get_size()
        self.width = 0.15 * self.window_width
        self.left_border = self.window_width - self.width 
        
        self.scale_rate = self.height / self.width 
        
        self.font = pygame.font.Font(None, int(50))
        self.background_color = (214, 189, 120)
        self.rect = pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        
        self.points = pygame.image.load('assets/menu/points.png').convert_alpha()
        self.points = pygame.transform.scale(self.points, (10* self.scale_rate, 10 * self.scale_rate))

        self.money = pygame.image.load('assets/menu/resources.png').convert_alpha()
        self.money = pygame.transform.scale(self.money, (10 * self.scale_rate, 10 * self.scale_rate))

        self.wave = pygame.image.load('assets/menu/wave.png').convert_alpha()
        self.wave = pygame.transform.scale(self.wave, (10 * self.scale_rate, 10 * self.scale_rate))

        self.hearth = pygame.image.load('assets/menu/lives.png').convert_alpha()
        self.hearth = pygame.transform.scale(self.hearth, (20 * self.scale_rate, 20 * self.scale_rate))
        
        self.play = pygame.image.load('assets/menu/play_button.png').convert()
        self.play = pygame.transform.scale(self.play, (60, 60))

        self.stop = pygame.image.load('assets/menu/stop_button.png').convert()
        self.stop = pygame.transform.scale(self.stop, (60, 60))
        
        self.speed_up = pygame.image.load('assets/menu/speed_up_button.png').convert()
        self.speed_up = pygame.transform.scale(self.speed_up, (60, 60))

        self.music = pygame.image.load('assets/menu/music.png').convert()
        self.music = pygame.transform.scale(self.music, (60, 60))
        
        scroll_image = pygame.image.load('assets/menu/play_button.png').convert()
        self.scroll_up = pygame.transform.rotate(scroll_image, 90)
        self.scroll_up = pygame.transform.scale(self.scroll_up, (30, 30))
        
        # self.scroll_down = pygame.image.load('assets/menu/play_button.png').convert()
        self.scroll_down = pygame.transform.rotate(scroll_image, 270)
        self.scroll_down = pygame.transform.scale(self.scroll_down, (30, 30))
        
        self.displayed_towers = [] # (img, name, price)
        self.displayed_towers_position = 0
        
        archer = pygame.image.load('assets/towers/archer_tower.png').convert_alpha()
        archer = pygame.transform.scale(archer, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((archer, "archer", 400))

        # Consider using tuple as one object atribute 
        magic = pygame.image.load('assets/towers/magic_tower.png').convert_alpha()
        magic = pygame.transform.scale(magic, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((magic, "magic", 300))
        
        cannon = pygame.image.load('assets/towers/cannon_tower.png').convert_alpha()
        cannon = pygame.transform.scale(cannon, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((cannon, "cannon", 500))
        
    def draw_all_menu(self, points, money, hearts, wave, game_paused):
        pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        pygame.draw.rect(self.screen, (0, 0, 0), (1360, 0, 1, self.height), 2)
        self.draw_points(points)
        self.draw_hearts(hearts)
        self.draw_money(money)
        self.draw_wave_counter(wave)

        if game_paused:
            self.game_pause_rect = self.screen.blit(self.play, (1380, 820))
        else:
            self.game_pause_rect = self.screen.blit(self.stop, (1380, 820))
            
        self.speed_up_rect = self.screen.blit(self.speed_up, (1450, 820))
        self.music_rect = self.screen.blit(self.music, (1520, 820))
        
        self.scroll_up_rect = self.screen.blit(self.scroll_up, (1465, 245))
        self.scroll_down_rect = self.screen.blit(self.scroll_down, (1465, 765))
        
        
        self.draw_towers_shop()

    def draw_towers_shop(self):
        
        if self.displayed_towers[self.displayed_towers_position]:
            
            tower_img, _, tower_price, = self.displayed_towers[self.displayed_towers_position]
            
            first_price = self.font.render(f'{tower_price}', True, (0, 0, 0))
            self.screen.blit(self.money, (self.left_border + self.width * 0.35 - 10 * self.scale_rate,  self.height * 0.52))
            self.screen.blit(first_price, (self.left_border + self.width * 0.4, self.height * 0.52)) 
            self.first_tower_rect = self.screen.blit(tower_img, (self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2, self.height * 0.32))

        if self.displayed_towers[self.displayed_towers_position + 1]:
            
            tower_img, _, tower_price, = self.displayed_towers[self.displayed_towers_position + 1]
            
            second_price = self.font.render(f'{tower_price}', True, (0, 0, 0))
            self.screen.blit(self.money, (self.left_border + self.width * 0.35 - 10 * self.scale_rate,  self.height * 0.8))
            self.screen.blit(second_price, (self.left_border + self.width * 0.4, self.height * 0.8)) 
            self.second_tower_rect = self.screen.blit(tower_img, (self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2, self.height * 0.6))

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


    def handle_click(self, clicked_position, game_paused):
        if (self.first_tower_rect.collidepoint(clicked_position)):
            return self.displayed_towers[self.displayed_towers_position]
        
        if (self.second_tower_rect.collidepoint(clicked_position)):
            return self.displayed_towers[self.displayed_towers_position + 1]
        
        if (self.game_pause_rect.collidepoint(clicked_position)):
            if game_paused:
                return None, "play", 0
            else:
                return None, "stop", 0
        
        if (self.speed_up_rect.collidepoint(clicked_position)):
            return None, "speed_up", 0
        
        if (self.music_rect.collidepoint(clicked_position)):
            return None, "music", 0
        
        if(self.scroll_up_rect.collidepoint(clicked_position)):
            if self.displayed_towers_position - 1 >= 0:
                self.displayed_towers_position -= 1
        
        if(self.scroll_down_rect.collidepoint(clicked_position)):
            if self.displayed_towers_position + 2 < len(self.displayed_towers):
                self.displayed_towers_position += 1

        return None, None, 0

        
