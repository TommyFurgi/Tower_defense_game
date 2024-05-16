import pygame

class Main_menu():
    def __init__(self, screen):
        self.width, self.height = screen.get_size()

        self.music = pygame.image.load('assets/menu/music.png').convert()
        self.music = pygame.transform.scale(self.music, (60, 60))

        knight = pygame.image.load('assets/knight.png').convert()
        self.knight = pygame.transform.scale(knight, (170, 500))

        self.font_buttons = pygame.font.Font(None, 24) 
        self.font_title = pygame.font.Font(None, 128)
        self.font_score = pygame.font.Font(None, 80)
        self.button_color = (83, 142, 237, 50)
        

        self.play_rect = pygame.Rect(0, 0, 0, 0)


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


    def draw_start_menu(self, screen, game_running):
        self.draw_back_tamplate((19, 9, 56, 255), 30, screen)
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

        self.music_rect = screen.blit(self.music, (1520, 820))


    def draw_end_menu(self, screen, player_won, score):
        self.draw_back_tamplate((19, 9, 56, 230), 30, screen)

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
        
        self.music_rect = screen.blit(self.music, (1520, 820))
        

    def handle_click_action(self, clicked_position, end_game, game_runnig):
        if (self.music_rect.collidepoint(clicked_position)):
            return "music"
        
        if (self.new_game_rect.collidepoint(clicked_position)):
            return "new_game"
        
        if not end_game:
            if game_runnig and (self.reasume_rect.collidepoint(clicked_position)):
                return "countinue"
        
        else:
            if self.return_to_menu_rect.collidepoint(clicked_position):
                return "back_to_menu"
            

        return None

        