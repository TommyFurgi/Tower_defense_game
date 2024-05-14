import pygame
 
class Map():
    def __init__(self, screen):
        self.screen = screen
        
        window_width, self.height = screen.get_size()
        self.width = 0.85 * window_width 

        self.background = pygame.image.load("assets/map.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.draw_background()

        self.font_buttons = pygame.font.Font(None, 24) 
        self.font_game_status = pygame.font.Font(None, 128)
        self.button_color = (83, 142, 237, 50)

        self.return_to_menu_rect = pygame.Rect(0, 0, 0, 0)
        self.restart_game_rect = pygame.Rect(0, 0, 0, 0)


    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        

    def draw_end_game_buttons(self, player_won):
        background = pygame.Surface((self.screen.get_width() - 400, self.screen.get_height() - 200), pygame.SRCALPHA)
        radius = 30  
        width, height = background.get_size()
        pygame.draw.circle(background, (19, 9, 56, 230), (radius, radius), radius)
        pygame.draw.circle(background, (19, 9, 56, 230), (width - radius, radius), radius)
        pygame.draw.circle(background, (19, 9, 56, 230), (radius, height - radius), radius)
        pygame.draw.circle(background, (19, 9, 56, 230), (width - radius, height - radius), radius)
        pygame.draw.rect(background, (19, 9, 56, 230), pygame.Rect(radius, 0, width - 2 * radius, height))
        pygame.draw.rect(background, (19, 9, 56, 230), pygame.Rect(0, radius, width, height - 2 * radius))

        self.screen.blit(background, (200, 100))

        if player_won:
            main_text = "Wygrałeś!!!"
        else:
            main_text = "Przegrałeś"

        text = self.font_game_status.render(main_text, True, (114, 179, 73))
        self.screen.blit(text, (self.width/2 - 150, self.height/2 - 150))


        self.return_to_menu_rect = pygame.Rect(self.width/2 - 130, self.height/2 + 100, 170, 70)
        pygame.draw.ellipse(self.screen, self.button_color, self.return_to_menu_rect)

        text = self.font_buttons.render("Powrót do menu", True, (255, 255, 255))
        self.screen.blit(text, (self.width/2 - 130 + 25, self.height/2 + 100 + 30))

        self.restart_game_rect = pygame.Rect(self.width/2 + 130, self.height/2 + 100, 170, 70)
        pygame.draw.ellipse(self.screen, self.button_color, self.restart_game_rect)

        text = self.font_buttons.render("Zagraj ponowenie", True, (255, 255, 255))
        self.screen.blit(text, (self.width/2 + 130 + 20, self.height/2 + 100 + 30))
        

    def handle_end_game_action(self, clicked_position):
        if self.restart_game_rect.collidepoint(clicked_position):
            return "restart"

        if self.return_to_menu_rect.collidepoint(clicked_position):
            return "back_to_menu"
        
        return None
    