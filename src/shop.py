import pygame
from resource_manager import ResourceManager

class Shop():
    def __init__(self, screen):
        '''
        Initialize the Menu object.

        Args:
            screen (pygame.Surface): The pygame screen surface object.
        '''
        self.screen = screen
        self.x_scale_rate = 1
        self.y_scale_rate = 1
        
        self.window_width, self.height = screen.get_size()
        self.width = 0.15 * self.window_width
        self.left_border = self.window_width - self.width 
        
        self.scale_rate = 3.75
        
        self.font = pygame.font.Font(None, int(50))
        self.background_color = (214, 189, 120)
        self.rect = pygame.draw.rect(self.screen, self.background_color, (self.left_border, 0, self.window_width, self.height))
        
        self.points = ResourceManager.get_image("points").convert_alpha()
        self.points_transformed = pygame.transform.scale(self.points, (10* self.scale_rate, 10 * self.scale_rate))

        self.money = ResourceManager.get_image("resources").convert_alpha()
        self.money_transformed = pygame.transform.scale(self.money, (10 * self.scale_rate, 10 * self.scale_rate))

        self.wave = ResourceManager.get_image("wave").convert_alpha()
        self.wave_transformed = pygame.transform.scale(self.wave, (10 * self.scale_rate, 10 * self.scale_rate))

        self.hearth = ResourceManager.get_image("lives").convert_alpha()
        self.hearth_transformed = pygame.transform.scale(self.hearth, (20 * self.scale_rate, 20 * self.scale_rate))
        
        self.play_button = ResourceManager.get_image("play_button").convert_alpha()
        self.play_transformed = pygame.transform.scale((self.play_button), (60, 60))

        self.stop = ResourceManager.get_image("stop_button").convert_alpha()
        self.stop_transformed = pygame.transform.scale(self.stop, (60, 60))
        
        self.speed_up = ResourceManager.get_image("speed_up_button").convert_alpha()
        self.speed_up_transformed = pygame.transform.scale(self.speed_up, (60, 60))

        self.music = ResourceManager.get_image("music").convert_alpha()
        self.music_transformed = pygame.transform.scale(self.music, (60, 60))
        
        self.scroll_up = pygame.transform.rotate(self.play_button, 90)
        self.scroll_up_transformed = pygame.transform.scale(self.scroll_up, (30, 30))
        
        self.scroll_down = pygame.transform.rotate(self.play_button, 270)
        self.scroll_down_transformed = pygame.transform.scale(self.scroll_down, (30, 30))
        
        self.displayed_towers = [] # (img, name, price)
        self.displayed_towers_position = 0
        
        archer = ResourceManager.get_image("archer_tower").convert_alpha()
        archer_transformed = pygame.transform.scale(archer, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((archer_transformed, "archer_tower", 400))

        magic = ResourceManager.get_image("magic_tower").convert_alpha()
        magic_transformed = pygame.transform.scale(magic, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((magic_transformed, "magic_tower", 300))
        
        cannon = ResourceManager.get_image("cannon_tower").convert_alpha()
        cannon_transformed = pygame.transform.scale(cannon, (41 * self.scale_rate, 41 * self.scale_rate))
        self.displayed_towers.append((cannon_transformed, "cannon_tower", 500))
        
    def draw_all_menu(self, points, money, hearts, wave, game_paused):
        '''
        Draw all elements of the menu on the screen.

        Args:
            points (int): The current points to display.
            money (int): The current money amount to display.
            hearts (int): The current number of lives to display.
            wave (int): The current wave number to display.
            game_paused (bool): Indicates if the game is paused or not.
        '''
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
        '''
        Draw the towers available for purchase in the shop.
        '''
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
        '''
        Draw the points indicator on the screen.

        Args:
            points (int): The current points to display.
        '''
        score = self.font.render(f'{points}', True, (0, 0, 0))
        self.screen.blit(self.points_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.16 * self.y_scale_rate))
        self.screen.blit(score, ((self.left_border + self.width * 0.3) * self.x_scale_rate, self.height * 0.16 * self.y_scale_rate))

    def draw_hearts(self, health_points):
        '''
        Draw the hearts indicating health on the screen.

        Args:
            health_points (int): The current health points to display.
        '''
        if (health_points > 0):
            self.screen.blit(self.hearth_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.01 * self.y_scale_rate))

        if (health_points > 1):
            self.screen.blit(self.hearth_transformed, ((self.left_border + self.width * 0.5 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.01 * self.y_scale_rate))

        if (health_points > 2):
            self.screen.blit(self.hearth_transformed, ((self.left_border + self.width * 0.8 - 10 * self.scale_rate) * self.x_scale_rate, self.height * 0.01 * self.y_scale_rate))
    
    def draw_money(self, money):
        '''
        Draw the money indicator on the screen.

        Args:
            money (int): The current amount of money to display.
        '''
        money = self.font.render(f'{money}', True, (0, 0, 0))
        self.screen.blit(self.money_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate,  self.height * 0.21 * self.y_scale_rate))
        self.screen.blit(money, ((self.left_border + self.width * 0.3) * self.x_scale_rate, self.height * 0.21 * self.y_scale_rate))        

    def draw_wave_counter(self, wave):
        '''
        Draw the wave counter on the screen.

        Args:
            wave (int): The current wave number to display.
        '''
        wave_text = self.font.render(f'{wave}', True, (0, 0, 0))
        self.screen.blit(self.wave_transformed, ((self.left_border + self.width * 0.2 - 10 * self.scale_rate) * self.x_scale_rate,  self.height * 0.11 * self.y_scale_rate))
        self.screen.blit(wave_text, ((self.left_border + self.width * 0.3) * self.x_scale_rate, self.height * 0.11 * self.y_scale_rate))        

    def handle_click(self, clicked_position, game_paused):
        '''
        Handle mouse clicks on interactive elements of the menu.

        Args:
            clicked_position (tuple): The (x, y) coordinates of the mouse click.
            game_paused (bool): Indicates if the game is currently paused.

        Returns:
            tuple or None: Depending on the clicked element, returns a tuple (img, name, price) or (None, action, 0).
        '''
        if self.first_tower_rect.collidepoint(clicked_position):
            return self.displayed_towers[self.displayed_towers_position]
        
        if self.second_tower_rect.collidepoint(clicked_position):
            return self.displayed_towers[self.displayed_towers_position + 1]
        
        if self.game_pause_rect.collidepoint(clicked_position):
            if game_paused:
                return None, "play", 0
            else:
                return None, "stop", 0
        
        if self.speed_up_rect.collidepoint(clicked_position):
            return None, "speed_up", 0
        
        if self.music_rect.collidepoint(clicked_position):
            return None, "music", 0
        
        if self.scroll_up_rect.collidepoint(clicked_position):
            if self.displayed_towers_position - 1 >= 0:
                self.displayed_towers_position -= 1
        
        if self.scroll_down_rect.collidepoint(clicked_position):
            if self.displayed_towers_position + 2 < len(self.displayed_towers):
                self.displayed_towers_position += 1

        return None, None, 0

    def scale_parameters(self, x_scale_rate, y_scale_rate):
        '''
        Scale all menu elements based on the provided scaling rates.

        Args:
            x_scale_rate (float): The scaling rate for the width.
            y_scale_rate (float): The scaling rate for the height.
        '''
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
        for img, name, price in self.displayed_towers:
            scaled_img = pygame.transform.scale(ResourceManager.get_image(name), (41 * self.scale_rate * x_scale_rate, 41 * self.scale_rate * y_scale_rate))
            scaled_towers.append((scaled_img, name, price))

        self.displayed_towers = scaled_towers