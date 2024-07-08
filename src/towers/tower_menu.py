import pygame
from towers.position import Position
from effects.effect_type import EffectType
from math import sqrt

class TowerMenu():
    """
    A class used to draw a tower menu.
    """
    def __init__(self, tower):
        self.tower = tower

        x_scale_rate, y_scale_rate = self.tower.x_scale_rate, tower.y_scale_rate

        self.sell_icon = pygame.image.load('assets/images/towers/sell_icon.png').convert_alpha()
        self.sell_icon_transformed = pygame.transform.scale(self.sell_icon, (50 * x_scale_rate, 50 * y_scale_rate))

        self.upgrade_icon = pygame.image.load('assets/images/towers/upgraded_icon.png').convert_alpha()
        self.upgrade_icon_transformed = pygame.transform.scale(self.upgrade_icon, (50 * x_scale_rate, 50 * y_scale_rate))
        self.font = pygame.font.Font(None, int(24 * x_scale_rate)) 
        
        self.arrow_right = pygame.image.load('assets/images/towers/arrow.png').convert_alpha()
        self.arrow_right_transformed = pygame.transform.scale(self.arrow_right, (30 * x_scale_rate, 30 * y_scale_rate))
        self.arrow_left = pygame.transform.rotate(self.arrow_right, 180)
        self.arrow_left_transformed = pygame.transform.scale(self.arrow_left, (30 * x_scale_rate, 30 * y_scale_rate))
        
        self.scale_rate = 1.3
        
        self.elipse_color = (133, 98, 42)
        self.elipse_width = 150 * x_scale_rate
        self.elipse_height = 60 * y_scale_rate
        
        self.text_color = (255, 255, 255)
        
        self.menu_pages = []
        self.current_menu_page = 0
    
    
    def draw(self, screen):
        """
        Calculates which positions from position.py aren't offscreen and
        based on that chooses appropriate number of menu pages and draws
        ellipses on them.
        """
        # Calculating ellipses positions
        tower_menu_positions = self.calculate_menu_positions()
            
        # Calculating positions where ellipses aren't off screen
        safe_positions = self.get_safe_positions(tower_menu_positions, screen)
            
        if not safe_positions:
            raise Exception("No safe positions for ellipses! (Shouldn't happen, check the code!)")
            
        # Creating list of functions that draw ellipses
        draw_ellipse_functions = self.get_draw_ellipse_fuctions()
            
        # Creating first page of tower menu        
        self.menu_pages = [self.create_tower_menu_surface()]
            
        current_position = 0
        current_page = 0
            
        for fn in draw_ellipse_functions:
            if current_position >= len(safe_positions):
                current_position = 0
                current_page += 1
                self.menu_pages.append(self.create_tower_menu_surface())
                
            fn(tower_menu_positions[safe_positions[current_position].value], self.menu_pages[current_page])
            current_position += 1
            
        self.draw_menu_change_arrows(safe_positions, self.menu_pages[self.current_menu_page])
  
        # Drawing tower_menu_surface on the screen
        screen.blit(self.menu_pages[self.current_menu_page], (self.tower.x - (self.tower.radius * 1.5 * self.scale_rate),
                                                              self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)))
    
    
    def draw_radius(self, tower_menu_surface):
        """Draws big circle around the tower."""
        pygame.draw.circle(tower_menu_surface, 
                           (0, 0, 255, 100), 
                           (self.tower.radius * self.scale_rate * 1.5, self.tower.radius * self.scale_rate * 1.5),
                            self.tower.radius * self.scale_rate, 0)  
        
        
    def prepare_ellipse(self, position):
        """Draws ellipse and returns it's rect and sufrace."""
        ell_rect = pygame.Rect(*position, self.elipse_width, self.elipse_height)
        ell_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        pygame.draw.ellipse(ell_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))
        
        return ell_rect, ell_surface
        
    def draw_cooldown_ellipse(self, position, tower_menu_surface):
        """Draws an ellipse with cooldown information."""
        cooldown_rect, cooldown_surface = self.prepare_ellipse(position)
        
        # Drawing cooldown info
        cooldown_text = self.font.render("Cooldown: " + str(int(self.tower.cooldown)), True, self.text_color)
        cooldown_surface.blit(cooldown_text, (self.elipse_width // 2 - cooldown_text.get_width() // 2, self.elipse_height // 2 - cooldown_text.get_height() // 2))
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(cooldown_surface, (cooldown_rect.x, cooldown_rect.y))


    def draw_damage_ellipse(self, position, tower_menu_surface):
        """Draws an ellipse with tower's damage and effects information."""
        damage_rect, damage_surface = self.prepare_ellipse(position)

        effect_names = {1 : "Poison", 2 : "Slow", 3 : "Boost"}
        offset = 0

        if self.tower.applied_effect:

            damage_text = self.font.render(effect_names[self.tower.applied_effect.value]
                                           + ": " + str(round(self.tower.effect_strength, 2)) + " / " + str(round(self.tower.effect_duration, 2)), True, self.text_color)
            damage_surface.blit(damage_text, (self.elipse_width // 2 - damage_text.get_width() // 2,
                                            self.elipse_height // 2 - damage_text.get_height() // 2 + 10))
            
            offset = -10
            
        damage_info_text = self.font.render("Damage: " + str(int(self.tower.damage)), True, self.text_color)
        damage_surface.blit(damage_info_text, (self.elipse_width // 2 - damage_info_text.get_width() // 2,
                                                         self.elipse_height // 2 - damage_info_text.get_height() // 2 + offset))
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(damage_surface, (damage_rect.x, damage_rect.y))


    def draw_damage_dealt_ellipse(self, position, tower_menu_surface):
        """Draws an ellipse with information about how many damage did tower deal."""
        damage_dealt_rect, damage_dealt_surface = self.prepare_ellipse(position)
        
        # Drawing the ellipse
        pygame.draw.ellipse(damage_dealt_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))

        # Drawing damage dealt info
        damage_dealt_info_text = self.font.render("Damage dealt:", True, self.text_color)
        damage_dealt_surface.blit(damage_dealt_info_text, (self.elipse_width // 2 - damage_dealt_info_text.get_width() // 2,
                                                         self.elipse_height // 2 - damage_dealt_info_text.get_height() // 2 - 10))
        # Drawing damage dealt amount
        damage_dealt = int(self.tower.damage_dealt)
        damage_dealt_str = str(damage_dealt)
        if int(damage_dealt) >= 1_000_000_000_000:
            damage_dealt_str = str(int(damage_dealt // 1_000_000_000_000)) + " T"
        elif int(damage_dealt) >= 1_000_000_000:
            damage_dealt_str = str(int(damage_dealt // 1_000_000_000)) + " B"
        elif int(damage_dealt) >= 1_000_000:
            damage_dealt_str = str(int(damage_dealt // 1_000_000)) + " M"
        elif int(damage_dealt) >= 1_000:
            damage_dealt_str = str(int(damage_dealt // 1_000)) + " K"
        else:
            damage_dealt_str = str(int(damage_dealt))

        damage_dealt_amount_text = self.font.render(damage_dealt_str, True, self.text_color)
        damage_dealt_surface.blit(damage_dealt_amount_text, (self.elipse_width // 2 - damage_dealt_amount_text.get_width() // 2,
                                                         self.elipse_height // 2 - damage_dealt_amount_text.get_height() // 2 + 10))
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(damage_dealt_surface, (damage_dealt_rect.x, damage_dealt_rect.y))
        

    def draw_target_mode_ellipse(self, position, tower_menu_surface):
        """
        Draws an ellipse with information about current targeting mode
        and arrows to change it.
        """
        # Tower target mode ellipse position
        target_mode_rect, target_mode_surface = self.prepare_ellipse(position)     

        # Drawing target mode info
        target_mode_info_text = self.font.render("Target:", True, self.text_color)
        target_mode_surface.blit(target_mode_info_text, (self.elipse_width // 2 - target_mode_info_text.get_width() // 2,
                                                         self.elipse_height // 2 - target_mode_info_text.get_height() // 2 - 10))

        # Drawing current target mode
        target_mode_text = self.font.render(self.tower.tower_target.value, True, self.text_color)
        target_mode_surface.blit(target_mode_text, (self.elipse_width // 2 - target_mode_text.get_width() // 2,
                                                    self.elipse_height // 2 - target_mode_text.get_height() // 2 + 10))

        # Drawing arrows and updating their position
        self.arrow_left_rect = target_mode_surface.blit(self.arrow_left_transformed, (0, self.elipse_height // 2 - self.arrow_left_transformed.get_height() // 2))
        self.arrow_left_rect.x += target_mode_rect.x + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
        self.arrow_left_rect.y += target_mode_rect.y + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
        
        self.arrow_right_rect = target_mode_surface.blit(self.arrow_right_transformed, (self.elipse_width - self.arrow_right_transformed.get_width(), self.elipse_height // 2 - self.arrow_right_transformed.get_height() // 2))
        self.arrow_right_rect.x += target_mode_rect.x + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
        self.arrow_right_rect.y += target_mode_rect.y + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(target_mode_surface, (target_mode_rect.x, target_mode_rect.y))


    def draw_sell_ellipse(self, position, tower_menu_surface):
        """Draws an ellipse with sell button and sell price information."""
        sell_rect, sell_ellipse_surface = self.prepare_ellipse(position)
        
        # Drawing the sell icon and updating its position
        self.sell_icon_rect = sell_ellipse_surface.blit(self.sell_icon_transformed, (0, 5))
        self.sell_icon_rect.x += sell_rect.x + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
        self.sell_icon_rect.y += sell_rect.y + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
        
        # Drawing sell price
        text = self.font.render("Price: " + str(self.tower.price), True, self.text_color)
        sell_ellipse_surface.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + 20, self.elipse_height // 2 - text.get_height() // 2))

        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(sell_ellipse_surface, (sell_rect.x, sell_rect.y))


    def draw_upgrade_ellipse(self, position, tower_menu_surface):
        """Draws an ellipse with upgrade button and upgrade price information."""
        if self.tower.level <= 3:

            upgrade_rect, upgrade_ellipse_surface = self.prepare_ellipse(position)
            
            # Drawing the upgrade icon and updating its position
            
            self.upgrade_icon_rect = upgrade_ellipse_surface.blit(self.upgrade_icon_transformed, (0, 5))
            self.upgrade_icon_rect.x += upgrade_rect.x + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
            self.upgrade_icon_rect.y += upgrade_rect.y + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
            
            # Drawing upgrade price
            text = self.font.render("Price: " + str(self.tower.price), True, self.text_color)
            upgrade_ellipse_surface.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + 20,self.elipse_height // 2 - text.get_height() // 2 + 10))

            # Drawing current level
            level_text = self.font.render("Level: " + str(self.tower.level), True, self.text_color)
            upgrade_ellipse_surface.blit(level_text, (self.elipse_width // 2 - text.get_width() // 2 + 20, self.elipse_height // 2 - text.get_height() // 2 - 10))

             # Blitting the ellipse on the tower_menu_surface
            tower_menu_surface.blit(upgrade_ellipse_surface, (upgrade_rect.x, upgrade_rect.y))


    def get_draw_ellipse_fuctions(self):
        """REturns a list of all possible ellipses"""
        return  [self.draw_upgrade_ellipse,
                 self.draw_sell_ellipse,
                 self.draw_target_mode_ellipse,
                 self.draw_cooldown_ellipse,
                 self.draw_damage_ellipse,
                 self.draw_damage_dealt_ellipse]
        
        

    def draw_menu_change_arrows(self, safe_positions, tower_menu_surface):
        """Draws two arrows responsible for changing menu's page."""
        # Tower damage ellipse position
        if  Position.TOP in safe_positions:
            change_rect = pygame.Rect(self.tower.radius * self.scale_rate * 1.5 - self.elipse_width // 2,
                                      self.tower.radius * self.scale_rate * 0.925 - self.elipse_height // 2,
                                      150, 60)
        elif Position.BOTTOM in safe_positions:
            change_rect = pygame.Rect(self.tower.radius * self.scale_rate * 1.5 - self.elipse_width // 2,
                                      self.tower.radius * self.scale_rate * 2.075 - self.elipse_height // 2,
                                      150, 60)
        elif Position.TOP_LEFT in safe_positions or Position.BOTTOM_LEFT in safe_positions:
            change_rect = pygame.Rect(self.tower.radius * self.scale_rate * 0.925 - self.elipse_width // 2,
                                      self.tower.radius * self.scale_rate * 1.5 - self.elipse_height // 2,
                                      150, 60)
        else:
            change_rect = pygame.Rect(self.tower.radius * self.scale_rate * 2.075 - self.elipse_width // 2,
                                      self.tower.radius * self.scale_rate * 1.5 - self.elipse_height // 2,
                                      150, 60)
        
        # Creating the ellipse surface
        change_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        pygame.draw.ellipse(change_surface, self.elipse_color, pygame.Rect(self.elipse_width // 4, self.elipse_height // 4, self.elipse_width // 2, self.elipse_height // 2))
    
        damage_text = self.font.render(str(self.current_menu_page + 1) + " / " + str(len(self.menu_pages)), True, self.text_color)
        change_surface.blit(damage_text, (self.elipse_width // 2 - damage_text.get_width() // 2,
                                          self.elipse_height // 2 - damage_text.get_height() // 2))
        
        # Drawing arrows and updating their position
        self.page_arrow_left_rect = change_surface.blit(self.arrow_left_transformed, (self.elipse_width // 6, self.elipse_height // 2 - self.arrow_left_transformed.get_height() // 2))
        self.page_arrow_left_rect.x += change_rect.x + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
        self.page_arrow_left_rect.y += change_rect.y + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
        
        self.page_arrow_right_rect = change_surface.blit(self.arrow_right_transformed, (self.elipse_width - self.arrow_right_transformed.get_width() - self.elipse_width // 6, self.elipse_height // 2 - self.arrow_right_transformed.get_height() // 2))
        self.page_arrow_right_rect.x += change_rect.x + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
        self.page_arrow_right_rect.y += change_rect.y + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(change_surface, (change_rect.x, change_rect.y))
    
    
    def calculate_menu_positions(self):
        """Decides where positions from position.py are relative to tower"""
        return [(self.tower.radius * self.scale_rate * 1.5 - self.elipse_width // 2, self.tower.radius * self.scale_rate * 0.45 ), # top
                (self.tower.radius * self.scale_rate * 1.95, self.tower.radius * self.scale_rate * 1), # top right
                (self.tower.radius * self.scale_rate * 1.95, self.tower.radius * self.scale_rate * 2 - self.elipse_height), # bottom right
                (self.tower.radius * self.scale_rate * 1.5 - self.elipse_width // 2, self.tower.radius * self.scale_rate * 2.55 - self.elipse_height), # bottom
                (self.tower.radius * self.scale_rate * 1 - self.elipse_width, self.tower.radius * self.scale_rate * 2 - self.elipse_height), # bottom left
                (self.tower.radius * self.scale_rate * 1 - self.elipse_width, self.tower.radius * self.scale_rate * 1)] # top left
    
    
    def create_tower_menu_surface(self):
        """Creates a surface for each menu page."""
        tower_menu_surface = pygame.Surface((self.tower.radius * 3 * self.scale_rate, self.tower.radius * 3 * self.scale_rate), pygame.SRCALPHA, 32)
        self.draw_radius(tower_menu_surface)
        return tower_menu_surface
    
    
    def get_safe_positions(self, tower_menu_positions, screen):
        """Calculates which positions in menu aren't off screen."""
        safe_positions = []

        for pos in Position:
            top_left_x = tower_menu_positions[pos.value][0] + self.tower.x - (self.tower.radius * 1.5 * self.scale_rate)
            top_left_y = tower_menu_positions[pos.value][1] + self.tower.y - (self.tower.radius * 1.5 * self.scale_rate)
            bottom_right_x = top_left_x + self.elipse_width
            bottom_right_y = top_left_y + self.elipse_height

            if (top_left_x >= 0 and bottom_right_x <= screen.get_width() * 0.85 and
                top_left_y >= 0 and bottom_right_y <= screen.get_height()):
                safe_positions.append(pos)

        return safe_positions
    
    def sell_pressed(self, clicked_position):
        """Checks if sell button was pressed."""
        return self.sell_icon_rect.collidepoint(clicked_position)
    
    def upgrade_pressed(self, clicked_position):
        """Checks if upgrade button was pressed."""
        return self.upgrade_icon_rect.collidepoint(clicked_position)
    
    def taget_mode_left_arrow_pressed(self, clicked_position):
        """Checks if left arrow used for changing targeting modes was pressed."""
        return self.arrow_left_rect.collidepoint(clicked_position)
    
    def taget_mode_right_arrow_pressed(self, clicked_position):
        """Checks if right arrow used for changing targeting modes was pressed."""
        return self.arrow_right_rect.collidepoint(clicked_position)
    
    def manage_tower_menu_page(self, clicked_position):
        """
        Checks if left or right arrow reponsible for changing menu page was pressed
        and then changes menu page if needed.
        """
        if self.page_arrow_left_rect.collidepoint(clicked_position):
            if self.current_menu_page > 0:
                self.current_menu_page -= 1
            return True
        
        if self.page_arrow_right_rect.collidepoint(clicked_position):
            if self.current_menu_page < len(self.menu_pages) - 1:
                self.current_menu_page += 1
            return True
        
        return False


    def scale_parameters(self):
        """
        Scales necessary parameters. Triggered when users
        resizes game window.
        """
        x_scale_rate, y_scale_rate = self.tower.x_scale_rate, self.tower.y_scale_rate
        
        self.font = pygame.font.Font(None, int(24 * x_scale_rate)) 
        self.sell_icon_transformed = pygame.transform.scale(self.sell_icon, (50 * x_scale_rate, 50 * y_scale_rate))
        self.upgrade_icon_transformed = pygame.transform.scale(self.upgrade_icon, (50 * x_scale_rate, 50 * y_scale_rate))
        self.arrow_right_transformed = pygame.transform.scale(self.arrow_right, (30 * x_scale_rate, 30 * y_scale_rate))
        self.arrow_left_transformed = pygame.transform.scale(self.arrow_left, (30 * x_scale_rate, 30 * y_scale_rate))

        self.elipse_width = 150 * x_scale_rate
        self.elipse_height = 60 * y_scale_rate


    