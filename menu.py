import pygame
from source_manager import SourceManager


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.x_scale_rate = 1
        self.y_scale_rate = 1
        
        self.window_width, self.height = screen.get_size()
        self.width = 0.15 * self.window_width
        self.left_border = self.window_width - self.width # 1360
        
        self.scale_rate = 3.75
        
        self.font = pygame.font.Font(None, int(50))
        self.background_color = (214, 189, 120)
        self.rect = pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        
        self.points = SourceManager.get_image("points").convert_alpha()
        self.points_transformed = pygame.transform.scale(self.points, (10* self.scale_rate, 10 * self.scale_rate))

        self.money = SourceManager.get_image("resources").convert_alpha()
        self.money_transformed = pygame.transform.scale(self.money, (10 * self.scale_rate, 10 * self.scale_rate))

        self.wave = SourceManager.get_image("wave").convert_alpha()
        self.wave_transformed = pygame.transform.scale(self.wave, (10 * self.scale_rate, 10 * self.scale_rate))

        self.hearth = SourceManager.get_image("lives").convert_alpha()
        self.hearth_transformed = pygame.transform.scale(self.hearth, (20 * self.scale_rate, 20 * self.scale_rate))
        
        self.play_button = SourceManager.get_image("play_button").convert_alpha()
        self.play_transformed = pygame.transform.scale((self.play_button), (60, 60))

        self.stop = SourceManager.get_image("stop_button").convert_alpha()
        self.stop_transformed = pygame.transform.scale(self.stop, (60, 60))
        
        self.speed_up = SourceManager.get_image("speed_up_button").convert_alpha()
        self.speed_up_transformed = pygame.transform.scale(self.speed_up, (60, 60))

        self.music = SourceManager.get_image("music").convert_alpha()
        self.music_transformed = pygame.transform.scale(self.music, (60, 60))
        
        self.scroll_up = pygame.transform.rotate(self.play_button, 90)
        self.scroll_up_transformed = pygame.transform.scale(self.scroll_up, (30, 30))
        
        self.scroll_down = pygame.transform.rotate(self.play_button, 270)
        self.scroll_down_transformed = pygame.transform.scale(self.scroll_down, (30, 30))
        
        self.displayed_towers = [] # (img, name, price)
        self.displayed_towers_position = 0
        
        archer = SourceManager.get_image("archer_tower").convert_alpha()
        archer_transformed = pygame.transform.scale(archer, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((archer_transformed, "archer_tower", 400))

        magic = SourceManager.get_image("magic_tower").convert_alpha()
        magic_transformed = pygame.transform.scale(magic, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((magic_transformed, "magic_tower", 300))
        
        cannon = SourceManager.get_image("cannon_tower").convert_alpha()
        cannon_transformed = pygame.transform.scale(cannon, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((cannon_transformed, "cannon_tower", 500))
        
    def draw_all_menu(self, points, money, hearts, wave, game_paused):
        pygame.draw.rect(self.screen, self.background_color, (self.left_border * self.x_scale_rate, 0, self.window_width * self.x_scale_rate, self.height * self.y_scale_rate))
        self.draw_points(points)
        self.draw_hearts(hearts)
        self.draw_money(money)
        self.draw_wave_counter(wave)

        if game_paused:
            self.game_pause_rect = self.screen.blit(self.play_transformed, (1380 * self.x_scale_rate, 820 * self.y_scale_rate))
        else:
            self.game_pause_rect = self.screen.blit(self.stop_transformed, (1380 * self.x_scale_rate, 820 * self.y_scale_rate))
            
        self.speed_up_rect = self.screen.blit(self.speed_up_transformed, (1450 * self.x_scale_rate, 820 * self.y_scale_rate))
        self.music_rect = self.screen.blit(self.music_transformed, (1520 * self.x_scale_rate, 820 * self.y_scale_rate))
        
        self.scroll_up_rect = self.screen.blit(self.scroll_up_transformed, (1465 * self.x_scale_rate, 245 * self.y_scale_rate))
        self.scroll_down_rect = self.screen.blit(self.scroll_down_transformed, (1465 * self.x_scale_rate, 765 * self.y_scale_rate))
        
        
        self.draw_towers_shop()

    def draw_towers_shop(self):
        
        if self.displayed_towers[self.displayed_towers_position]:
            
            tower_img, _, tower_price, = self.displayed_towers[self.displayed_towers_position]
            
            first_price = self.font.render(f'{tower_price}', True, (0, 0, 0))
            self.screen.blit(self.money_transformed, ((self.left_border + self.width * 0.35 - 10 * self.scale_rate) * self.x_scale_rate,  self.height * 0.52 * self.y_scale_rate))
            self.screen.blit(first_price, ((self.left_border + self.width * 0.4) * self.x_scale_rate, self.height * 0.52 * self.y_scale_rate)) 
            self.first_tower_rect = self.screen.blit(tower_img, ((self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2) * self.x_scale_rate, self.height * 0.32 * self.y_scale_rate))

        if self.displayed_towers[self.displayed_towers_position + 1]:
            
            tower_img, _, tower_price, = self.displayed_towers[self.displayed_towers_position + 1]
            
            second_price = self.font.render(f'{tower_price}', True, (0, 0, 0))
            self.screen.blit(self.money_transformed, ((self.left_border + self.width * 0.35 - 10 * self.scale_rate) * self.x_scale_rate,  self.height * 0.8 * self.y_scale_rate))
            self.screen.blit(second_price, ((self.left_border + self.width * 0.4) * self.x_scale_rate, self.height * 0.8 * self.y_scale_rate)) 
            self.second_tower_rect = self.screen.blit(tower_img, ((self.left_border + self.width * 0.5 - (41 * self.scale_rate) / 2) * self.x_scale_rate, self.height * 0.6 * self.y_scale_rate))

    def draw_points(self, points):
        score = self.font.render(f'{points}', True, (0, 0, 0))
        self.screen.blit(self.points_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.16 * self.y_scale_rate))
        self.screen.blit(score, ((self.left_border + self.width * 0.3) * self.x_scale_rate, self.height * 0.16 * self.y_scale_rate))

    def draw_hearts(self, health_points):
        if (health_points > 0):
            self.screen.blit(self.hearth_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.01 * self.y_scale_rate))

        if (health_points > 1):
            self.screen.blit(self.hearth_transformed, ((self.left_border + self.width * 0.5 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.01 * self.y_scale_rate))

        if (health_points > 2):
            self.screen.blit(self.hearth_transformed, ((self.left_border + self.width * 0.8 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.01 * self.y_scale_rate))
    
    def draw_money(self, money):
        money = self.font.render(f'{money}', True, (0, 0, 0))
        self.screen.blit(self.money_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate,  self.height * 0.21 * self.y_scale_rate))
        self.screen.blit(money, ((self.left_border + self.width * 0.3) * self.x_scale_rate, self.height * 0.21 * self.y_scale_rate))        

    def draw_wave_counter(self, wave):
        wave = self.font.render(f'{wave}', True, (0, 0, 0))
        self.screen.blit(self.wave_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate,  self.height * 0.11 * self.y_scale_rate))
        self.screen.blit(wave, ((self.left_border + self.width * 0.3) * self.x_scale_rate, self.height * 0.11 * self.y_scale_rate))        


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

        
    def scale_parameters(self, x_scale_rate, y_scale_rate):
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.rect = pygame.draw.rect(self.screen, self.background_color, (self.left_border * x_scale_rate, 0, self.window_width * x_scale_rate, self.height * y_scale_rate))
        self.font = pygame.font.Font(None, int(50 * x_scale_rate))

        self.points_transformed = pygame.transform.scale(self.points, (10 * self.scale_rate * x_scale_rate, 10 * self.scale_rate * y_scale_rate))
        self.money_transformed = pygame.transform.scale(self.money, (10 * self.scale_rate * x_scale_rate, 10 * self.scale_rate * y_scale_rate))
        self.wave_transformed = pygame.transform.scale(self.wave, (10 * self.scale_rate * x_scale_rate, 10 * self.scale_rate * y_scale_rate))
        self.hearth_transformed = pygame.transform.scale(self.hearth, (20 * self.scale_rate * x_scale_rate, 20 * self.scale_rate * y_scale_rate))
        self.play_transformed = pygame.transform.scale(self.play_button, (60 * x_scale_rate, 60 * y_scale_rate))
        self.stop_transformed = pygame.transform.scale(self.stop, (60 * x_scale_rate, 60 * y_scale_rate))
        self.speed_up_transformed = pygame.transform.scale(self.speed_up, (60 * x_scale_rate, 60 * y_scale_rate))
        self.music_transformed = pygame.transform.scale(self.music, (60 * x_scale_rate, 60 * y_scale_rate))
        self.scroll_up_transformed = pygame.transform.scale(self.scroll_up, (30 * x_scale_rate, 30 * y_scale_rate))
        self.scroll_down_transformed = pygame.transform.scale(self.scroll_down, (30 * x_scale_rate, 30 * y_scale_rate))

        scaled_towers = []
        for _, name, price in self.displayed_towers:
            scaled_img = pygame.transform.scale(SourceManager.get_image(name), (41 * self.scale_rate * x_scale_rate, 41 * self.scale_rate * y_scale_rate))
            scaled_towers.append((scaled_img, name, price))

        self.displayed_towers = scaled_towers