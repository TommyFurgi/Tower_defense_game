import pygame
from source_manager import SourceManager


class Main_menu():
    def __init__(self, screen):
        self.width, self.height = screen.get_size()

        self.music = SourceManager.get_image("music2").convert()
        self.music = pygame.transform.scale(self.music, (100, 100))

        self.knight = SourceManager.get_image("knight").convert()
        self.knight = pygame.transform.scale(self.knight, (170, 500))

        self.info = SourceManager.get_image("question").convert()
        self.info = pygame.transform.scale(self.info, (100, 100))

        self.back = SourceManager.get_image("back").convert()
        self.back = pygame.transform.scale(self.back, (100, 100))

        self.instruction = SourceManager.get_image("instruction").convert()

        self.font_buttons = pygame.font.Font(None, 24) 
        self.font_title = pygame.font.Font(None, 128)
        self.font_score = pygame.font.Font(None, 80)
        self.button_color = (83, 142, 237, 50)
        
        self.play_rect = pygame.Rect(0, 0, 0, 0)

        self.show_info = False


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
        self.draw_back_tamplate((19, 9, 56, 255), 30, screen)
        self.music_rect = screen.blit(self.music, (220 , 680))
        self.info_rect = screen.blit(self.info, (220, 560))

        if self.show_info:
            self.draw_info_menu(screen)
        elif player_won != None: 
            self.draw_end_menu(screen, player_won, points)
        else:
            self.draw_start_menu(screen, game_running)


    def draw_back_tamplate(self, color, radius, screen):
        background = pygame.Surface((self.width - 400, self.height - 200), pygame.SRCALPHA)
        width, height = background.get_size()
        pygame.draw.circle(background, color, (radius, radius), radius)
        pygame.draw.circle(background, color, (width - radius, radius), radius)
        pygame.draw.circle(background, color, (radius, height - radius), radius)
        pygame.draw.circle(background, color, (width - radius, height - radius), radius)
        pygame.draw.rect(background, color, pygame.Rect(radius, 0, width - 2 * radius, height))
        pygame.draw.rect(background, color, pygame.Rect(0, radius, width, height - 2 * radius))

        screen.blit(background, (200, 100))

        self.music_rect = screen.blit(self.music, (220 , 680))
        self.info_rect = screen.blit(self.info, (220, 560))


    def draw_start_menu(self, screen, game_running):
        screen.blit(self.knight, (1050, 300))

        text = self.font_title.render("Witaj rycerzu!", True, (114, 179, 73))
        screen.blit(text, (self.width/2 - 450, self.height/2 - 170))

        self.new_game_rect = pygame.Rect(self.width/2 - 300, self.height/2 + 50, 220, 70)
        pygame.draw.ellipse(screen, self.button_color, self.new_game_rect)

        text = self.font_buttons.render("Nowa gra", True, (255, 255, 255))
        screen.blit(text, (self.width/2 - 300 + 65, self.height/2 + 50 + 25))

        if game_running:
            self.reasume_rect = pygame.Rect(self.width/2 - 300, self.height/2 + 150, 220, 70)
            pygame.draw.ellipse(screen, self.button_color, self.reasume_rect)

            text = self.font_buttons.render("Kontynuuj", True, (255, 255, 255))
            screen.blit(text, (self.width/2 - 300 + 60, self.height/2 + 150 + 25))


    def draw_end_menu(self, screen, player_won, score):
        self.draw_back_tamplate((19, 9, 56, 255), 30, screen)

        if player_won:
            main_text = "Wygrałeś!!!"
        else:
            main_text = "Przegrałeś"

        text = self.font_title.render(main_text, True, (114, 179, 73))
        screen.blit(text, (self.width/2 - 220, self.height/2 - 200))

        text = self.font_score.render("Twój wynik to: " + str(score), True, (114, 179, 73))
        screen.blit(text, (self.width/2 - 250, self.height/2 - 70))

        self.return_to_menu_rect = pygame.Rect(self.width/2 - 110 - 220, self.height/2 + 100, 220, 70)
        pygame.draw.ellipse(screen, self.button_color, self.return_to_menu_rect)

        text = self.font_buttons.render("Powrót do menu", True, (255, 255, 255))
        screen.blit(text, (self.width/2 - 110 - 220 + 40, self.height/2 + 100 + 30))

        self.new_game_rect = pygame.Rect(self.width/2 + 110, self.height/2 + 100, 220, 70)
        pygame.draw.ellipse(screen, self.button_color, self.new_game_rect)

        text = self.font_buttons.render("Zagraj ponowenie", True, (255, 255, 255))
        screen.blit(text, (self.width/2 + 110 + 40, self.height/2 + 100 + 30))
        

    def draw_info_menu(self, screen):
        self.draw_back_tamplate((19, 9, 56, 255), 30, screen)
        self.back_rect = screen.blit(self.back, (220, 440))
        screen.blit(self.instruction, (320, 115))
        

    def handle_click_action(self, clicked_position, end_game, game_runnig):
        if (self.music_rect.collidepoint(clicked_position)):
            return "music"
        
        if (self.new_game_rect.collidepoint(clicked_position)):
            return "new_game"
        
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

        