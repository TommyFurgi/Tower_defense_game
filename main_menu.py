import pygame
from source_manager import SourceManager


class Main_menu():
    def __init__(self, screen):
        self.x_scale_rate = 1
        self.y_scale_rate = 1
        self.width, self.height = screen.get_size()

        self.music = SourceManager.get_image("music2").convert()
        self.music_transformed = pygame.transform.scale(self.music, (100, 100))

        self.knight = SourceManager.get_image("knight").convert()
        self.knight_transformed = pygame.transform.scale(self.knight, (170, 500))

        self.info = SourceManager.get_image("question").convert()
        self.info_transformed = pygame.transform.scale(self.info, (100, 100))

        self.back = SourceManager.get_image("back").convert()
        self.back_transformed = pygame.transform.scale(self.back, (100, 100))

        self.instruction = SourceManager.get_image("instruction").convert()
        self.instruction_transformed = pygame.transform.scale(self.instruction, (1052, 657))

        self.font_buttons = pygame.font.Font(None, 24) 
        self.font_title = pygame.font.Font(None, 128)
        self.font_score = pygame.font.Font(None, 80)
        self.button_color = (83, 142, 237, 50)
        
        self.play_rect = pygame.Rect(0, 0, 0, 0)

        self.show_info = False
        self.elipse_width = 220 * self.x_scale_rate
        self.elipse_height = 70 * self.y_scale_rate

    # Getter
    @property
    def show_info(self):
        return self._show_info
    

    # Setter
    @show_info.setter
    def show_info(self, value):
        if not isinstance(value, bool):
            raise ValueError("Wartość show_info musi być typu bool")
        self._show_info = value


    def draw_main_menu(self, screen, game_running, player_won, points):
        self.draw_back_tamplate((19, 9, 56, 255), 30 * self.x_scale_rate, screen)
        self.music_rect = screen.blit(self.music_transformed, (220 * self.x_scale_rate, 680 * self.y_scale_rate))
        self.info_rect = screen.blit(self.info_transformed, (220 * self.x_scale_rate, 560 * self.y_scale_rate))

        if self.show_info:
            self.draw_info_menu(screen)
        elif player_won != None: 
            self.draw_end_menu(screen, player_won, points)
        else:
            self.draw_start_menu(screen, game_running)


    def draw_back_tamplate(self, color, radius, screen):
        background = pygame.Surface(((self.width - 400) * self.x_scale_rate, (self.height - 200) * self.y_scale_rate), pygame.SRCALPHA)
        width, height = background.get_size()
        pygame.draw.circle(background, color, (radius, radius), radius)
        pygame.draw.circle(background, color, (width - radius, radius), radius)
        pygame.draw.circle(background, color, (radius, height - radius), radius)
        pygame.draw.circle(background, color, (width - radius, height - radius), radius)
        pygame.draw.rect(background, color, pygame.Rect(radius, 0, width - 2 * radius, height))
        pygame.draw.rect(background, color, pygame.Rect(0, radius, width, height - 2 * radius))

        screen.blit(background, (200 * self.x_scale_rate, 100 * self.y_scale_rate))

    def draw_start_menu(self, screen, game_running):
        screen.blit(self.knight_transformed, (1050 * self.x_scale_rate, 300 * self.y_scale_rate))

        text = self.font_title.render("Hello Knight!", True, (114, 179, 73))
        screen.blit(text, ((self.width/2 - 450) * self.x_scale_rate, (self.height/2 - 170) * self.y_scale_rate))

        if game_running:
            self.reasume_rect = pygame.Rect((self.width/2 - 300) * self.x_scale_rate, (self.height/2 + 30)  * self.y_scale_rate, self.elipse_width, self.elipse_height)
            pygame.draw.ellipse(screen, self.button_color, self.reasume_rect)

            text = self.font_buttons.render("Resume", True, (255, 255, 255))
            screen.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + (self.width/2 - 300) * self.x_scale_rate, self.elipse_height // 2 - text.get_height() // 2 + (self.height/2 + 30) * self.y_scale_rate))

    
        self.new_game_rect = pygame.Rect((self.width/2 - 300) * self.x_scale_rate, (self.height/2 + 130) * self.y_scale_rate, self.elipse_width, self.elipse_height)
        pygame.draw.ellipse(screen, self.button_color, self.new_game_rect)

        text = self.font_buttons.render("New game", True, (255, 255, 255))
        screen.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + (self.width/2 - 300) * self.x_scale_rate, self.elipse_height // 2 - text.get_height() // 2 + (self.height/2 + 130) * self.y_scale_rate))

        self.exit_rect = pygame.Rect((self.width/2 - 300) * self.x_scale_rate, (self.height/2 + 230) * self.y_scale_rate, self.elipse_width, self.elipse_height)
        pygame.draw.ellipse(screen, self.button_color, self.exit_rect)

        text = self.font_buttons.render("Exit", True, (255, 255, 255))
        screen.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + (self.width/2 - 300) * self.x_scale_rate, self.elipse_height // 2 - text.get_height() // 2 + (self.height/2 + 230) * self.y_scale_rate))


    def draw_end_menu(self, screen, player_won, score):
        if player_won:
            main_text = "You won!!!"
        else:
            main_text = "You lost"

        text = self.font_title.render(main_text, True, (114, 179, 73))
        screen.blit(text, (self.width/2 * self.x_scale_rate - text.get_width()//2, (self.height/2 - 200) * self.y_scale_rate))

        text = self.font_score.render("Your result: " + str(score), True, (114, 179, 73))
        screen.blit(text, (self.width/2* self.x_scale_rate - text.get_width()//2, (self.height/2 - 70) * self.y_scale_rate))

        self.return_to_menu_rect = pygame.Rect((self.width/2 - 330) * self.x_scale_rate, (self.height/2 + 100) * self.y_scale_rate, self.elipse_width, self.elipse_height)
        pygame.draw.ellipse(screen, self.button_color, self.return_to_menu_rect)

        text = self.font_buttons.render("Back to menu", True, (255, 255, 255))
        screen.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + (self.width/2 - 110) * self.x_scale_rate - self.elipse_width, self.elipse_height // 2 - text.get_height() // 2 + (self.height/2 + 100) * self.y_scale_rate))

        self.new_game_rect = pygame.Rect((self.width/2 + 110) * self.x_scale_rate, (self.height/2 + 100) * self.y_scale_rate, self.elipse_width, self.elipse_height)
        pygame.draw.ellipse(screen, self.button_color, self.new_game_rect)

        text = self.font_buttons.render("Play again", True, (255, 255, 255))
        screen.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + (self.width/2 + 110) * self.x_scale_rate, self.elipse_height // 2 - text.get_height() // 2 + (self.height/2 + 100) * self.y_scale_rate))
        

    def draw_info_menu(self, screen):
        self.back_rect = screen.blit(self.back_transformed, (220 * self.x_scale_rate, 440 * self.y_scale_rate))
        screen.blit(self.instruction_transformed, (320 * self.x_scale_rate, 115 * self.y_scale_rate))
        

    def handle_click_action(self, clicked_position, end_game, game_runnig):
        if (self.music_rect.collidepoint(clicked_position)):
            return "music"
        
        if (self.new_game_rect.collidepoint(clicked_position)):
            return "new_game"
        
        if (self.exit_rect.collidepoint(clicked_position)):
            return "exit_game"
        
        if (self.info_rect.collidepoint(clicked_position)):
            self.show_info = True
            return None
        
        if self.show_info:
            if (self.back_rect.collidepoint(clicked_position)):
                self.show_info = False
                return None
        
        if not end_game:
            if game_runnig and (self.reasume_rect.collidepoint(clicked_position)):
                return "countinue"
        
        else:
            if self.return_to_menu_rect.collidepoint(clicked_position):
                return "back_to_menu"
            
        return None

    def scale_parameters(self, x_scale_rate, y_scale_rate):
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.music_transformed = pygame.transform.scale(self.music, (100 * x_scale_rate, 100 * y_scale_rate))
        self.knight_transformed = pygame.transform.scale(self.knight, (170 * x_scale_rate, 500 * y_scale_rate))
        self.info_transformed = pygame.transform.scale(self.info, (100 * x_scale_rate, 100 * y_scale_rate))
        self.back_transformed = pygame.transform.scale(self.back, (100 * x_scale_rate, 100 * y_scale_rate))
        self.instruction_transformed = pygame.transform.scale(self.instruction, (1052 * x_scale_rate, 657 * y_scale_rate))

        self.font_buttons = pygame.font.Font(None, int(24 * x_scale_rate)) 
        self.font_title = pygame.font.Font(None, int(128 * x_scale_rate))
        self.font_score = pygame.font.Font(None, int(80 * x_scale_rate))

        self.elipse_width = 220 * self.x_scale_rate
        self.elipse_height = 70 * self.y_scale_rate