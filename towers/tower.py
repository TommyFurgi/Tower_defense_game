import pygame
from abc import ABC
from text_alert import TextAlert
from towers.target import Target
from towers.position import Position
from source_manager import SourceManager

class Tower(pygame.sprite.Sprite, ABC): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.level = 1
        self.selected = False

        self.damage_dealt = 0

        self.tower_target = Target.NOT_SET

        self.target_modes = []
        self.current_target_mode = 0

        self.time_from_last_shot = pygame.time.get_ticks()

        sell_icon = pygame.image.load('assets/images/towers/sell_icon.png').convert_alpha()
        self.sell_icon = pygame.transform.scale(sell_icon, (50, 50))

        upgrade_icon = pygame.image.load('assets/images/towers/upgraded_icon.png').convert_alpha()
        self.upgrade_icon = pygame.transform.scale(upgrade_icon, (50, 50))
        self.font = pygame.font.Font(None, 24) 
        
        self.arrow_icon = pygame.image.load('assets/images/towers/arrow.png').convert_alpha()
        self.arrow_right = pygame.transform.scale(self.arrow_icon, (30, 30))
        self.arrow_left = pygame.transform.rotate(self.arrow_icon, 180)
        self.arrow_left = pygame.transform.scale(self.arrow_left, (30, 30))

        self.sell_sound = SourceManager.get_sound("selling")
        self.upgrade_sound = SourceManager.get_sound("upgrade")
        
        self.scale_rate = 1.3
        
        self.elipse_color = (133, 98, 42)
        self.elipse_width = 150
        self.elipse_height = 60
        
        self.text_color = (255, 255, 255)
        
        self.menu_pages = []
        self.current_menu_page = 0
        
        

    def draw(self, screen, delta_time):
        screen.blit(self.image, (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))

    def draw_radius(self, tower_menu_surface):

        pygame.draw.circle(tower_menu_surface, (0, 0, 255, 100), (self.radius * self.scale_rate * 1.5,
                                                                  self.radius * self.scale_rate * 1.5),
                                                                  self.radius * self.scale_rate, 0)    

    def draw_cooldown_ellipse(self, position, tower_menu_surface):
        
        # Tower cooldown ellipse position
        cooldown_rect = pygame.Rect(*position, 150, 60)
        
        # Creating the ellipse surface
        cooldown_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        # Drawing the ellipse
        pygame.draw.ellipse(cooldown_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))
        
        # Drawing cooldown info
        cooldown_text = self.font.render("Cooldown: " + str(int(self.cooldown)), True, self.text_color)
        cooldown_surface.blit(cooldown_text, (self.elipse_width // 2 - cooldown_text.get_width() // 2, self.elipse_height // 2 - cooldown_text.get_height() // 2))
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(cooldown_surface, (cooldown_rect.x, cooldown_rect.y))

    def draw_damage_ellipse(self, position, tower_menu_surface):
        
        # Tower damage ellipse position
        damage_rect = pygame.Rect(*position, 150, 60)
        
        # Creating the ellipse surface
        damage_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        pygame.draw.ellipse(damage_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))

        damage_text = self.font.render("Damage: " + str(int(self.damage)), True, self.text_color)
        damage_surface.blit(damage_text, (self.elipse_width // 2 - damage_text.get_width() // 2,
                                          self.elipse_height // 2 - damage_text.get_height() // 2))
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(damage_surface, (damage_rect.x, damage_rect.y))

    def draw_damage_dealt_ellipse(self, position, tower_menu_surface):
        # Tower damage dealt ellipse position
        damage_dealt_rect = pygame.Rect(*position, 150, 60)
        
        # Creating the ellipse surface
        damage_dealt_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        # Drawing the ellipse
        pygame.draw.ellipse(damage_dealt_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))

        # Drawing damage dealt info
        damage_dealt_info_text = self.font.render("Damage dealt:", True, self.text_color)
        damage_dealt_surface.blit(damage_dealt_info_text, (self.elipse_width // 2 - damage_dealt_info_text.get_width() // 2,
                                                         self.elipse_height // 2 - damage_dealt_info_text.get_height() // 2 - 10))
        # Drawing damage dealt amount
        damage_dealt_str = str(int(self.damage_dealt))
        if int(self.damage_dealt) >= 1_000_000_000_000:
            damage_dealt_str = str(int(self.damage_dealt // 1_000_000_000_000)) + " T"
        elif int(self.damage_dealt) >= 1_000_000_000:
            damage_dealt_str = str(int(self.damage_dealt // 1_000_000_000)) + " B"
        elif int(self.damage_dealt) >= 1_000_000:
            damage_dealt_str = str(int(self.damage_dealt // 1_000_000)) + " M"
        elif int(self.damage_dealt) >= 1_000:
            damage_dealt_str = str(int(self.damage_dealt // 1_000)) + " K"
        else:
            damage_dealt_str = str(int(self.damage_dealt))

        damage_dealt_amount_text = self.font.render(damage_dealt_str, True, self.text_color)
        damage_dealt_surface.blit(damage_dealt_amount_text, (self.elipse_width // 2 - damage_dealt_amount_text.get_width() // 2,
                                                         self.elipse_height // 2 - damage_dealt_amount_text.get_height() // 2 + 10))
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(damage_dealt_surface, (damage_dealt_rect.x, damage_dealt_rect.y))
        

    def draw_target_mode_ellipse(self, position, tower_menu_surface):
        # Tower target mode ellipse position
        target_mode_rect = pygame.Rect(*position, 150, 60)
        
        # Creating the ellipse surface
        target_mode_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        # Drawing the elipse
        pygame.draw.ellipse(target_mode_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))        

        # Drawing target mode info
        target_mode_info_text = self.font.render("Target:", True, self.text_color)
        target_mode_surface.blit(target_mode_info_text, (self.elipse_width // 2 - target_mode_info_text.get_width() // 2,
                                                         self.elipse_height // 2 - target_mode_info_text.get_height() // 2 - 10))

        # Drawing current target mode
        target_mode_text = self.font.render(self.tower_target.value, True, self.text_color)
        target_mode_surface.blit(target_mode_text, (self.elipse_width // 2 - target_mode_text.get_width() // 2,
                                                    self.elipse_height // 2 - target_mode_text.get_height() // 2 + 10))

        # Drawing arrows and updating their position
        self.arrow_left_rect = target_mode_surface.blit(self.arrow_left, (0, self.elipse_height // 2 - self.arrow_left.get_height() // 2))
        self.arrow_left_rect.x += target_mode_rect.x + self.x - (self.radius * 1.5 * self.scale_rate)
        self.arrow_left_rect.y += target_mode_rect.y + self.y - (self.radius * 1.5 * self.scale_rate)
        
        self.arrow_right_rect = target_mode_surface.blit(self.arrow_right, (self.elipse_width - self.arrow_right.get_width(), self.elipse_height // 2 - self.arrow_right.get_height() // 2))
        self.arrow_right_rect.x += target_mode_rect.x + self.x - (self.radius * 1.5 * self.scale_rate)
        self.arrow_right_rect.y += target_mode_rect.y + self.y - (self.radius * 1.5 * self.scale_rate)
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(target_mode_surface, (target_mode_rect.x, target_mode_rect.y))


    def draw_sell_ellipse(self, position, tower_menu_surface):
        # Tower selling ellipse position
        sell_rect = pygame.Rect(*position, 150, 60)
        
        # Creating the ellipse surface
        sell_ellipse_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        # Drawing the ellipse
        pygame.draw.ellipse(sell_ellipse_surface, self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))
        
        # Drawing the sell icon and updating its position
        self.sell_icon_rect = sell_ellipse_surface.blit(self.sell_icon, (0, 5))
        self.sell_icon_rect.x += sell_rect.x + self.x - (self.radius * 1.5 * self.scale_rate)
        self.sell_icon_rect.y += sell_rect.y + self.y - (self.radius * 1.5 * self.scale_rate)
        
        # Drawing sell price
        text = self.font.render("Price: " + str(self.price), True, self.text_color)
        sell_ellipse_surface.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + 20, self.elipse_height // 2 - text.get_height() // 2))

        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(sell_ellipse_surface, (sell_rect.x, sell_rect.y))

    def draw_upgrade_ellipse(self, position, tower_menu_surface):
        
        if self.level <= 3:
            # Tower upgrading ellips position
            upgrade_rect = pygame.Rect(*position, 150, 60)
            
            # Creating the ellipse surface
            upgrade_ellipse_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
            
            # Drawing the ellipse
            pygame.draw.ellipse(upgrade_ellipse_surface,self.elipse_color, pygame.Rect(0, 0, self.elipse_width, self.elipse_height))
            
            # Drawing the upgrade icon and updating its position
            self.upgrade_icon_rect = upgrade_ellipse_surface.blit(self.upgrade_icon, (0, 5))
            self.upgrade_icon_rect.x += upgrade_rect.x + self.x - (self.radius * 1.5 * self.scale_rate)
            self.upgrade_icon_rect.y += upgrade_rect.y + self.y - (self.radius * 1.5 * self.scale_rate)
            
            # Drawing upgrade price
            text = self.font.render("Price: " + str(self.price), True, self.text_color)
            upgrade_ellipse_surface.blit(text, (self.elipse_width // 2 - text.get_width() // 2 + 20,self.elipse_height // 2 - text.get_height() // 2 + 10))

            # Drawing current level
            level_text = self.font.render("Level: " + str(self.level), True, self.text_color)
            upgrade_ellipse_surface.blit(level_text, (self.elipse_width // 2 - text.get_width() // 2 + 20, self.elipse_height // 2 - text.get_height() // 2 - 10))

             # Blitting the ellipse on the tower_menu_surface
            tower_menu_surface.blit(upgrade_ellipse_surface, (upgrade_rect.x, upgrade_rect.y))

    
    def create_tower_menu_surface(self):
        
        tower_menu_surface = pygame.Surface((self.radius * 3 * self.scale_rate, self.radius * 3 * self.scale_rate), pygame.SRCALPHA, 32)
        self.draw_radius(tower_menu_surface)
          
        return tower_menu_surface  
    
    def calculate_menu_positions(self):
        
        return [
                (self.radius * self.scale_rate * 1.5 - self.elipse_width // 2, self.radius * self.scale_rate * 0.45), # top
                (self.radius * self.scale_rate * 1.95, self.radius * self.scale_rate * 1), # top right
                (self.radius * self.scale_rate * 1.95, self.radius * self.scale_rate * 2 - self.elipse_height), # bottom right
                (self.radius * self.scale_rate * 1.5 - self.elipse_width // 2, self.radius * self.scale_rate * 2.55 - self.elipse_height), # bottom
                (self.radius * self.scale_rate * 1 - self.elipse_width, self.radius * self.scale_rate * 2 - self.elipse_height), # bottom left
                (self.radius * self.scale_rate * 1 - self.elipse_width, self.radius * self.scale_rate * 1), # top left
            ]
        
    
    def draw_menu_change_arrows(self, position, tower_menu_surface):
        
        # Tower damage ellipse position
        if position == Position.TOP.value:
            change_rect = pygame.Rect(self.radius * self.scale_rate * 1.5 - self.elipse_width // 2,
                                      self.radius * self.scale_rate * 0.925 - self.elipse_height // 2,
                                      150, 60)
        else:
            change_rect = pygame.Rect(self.radius * self.scale_rate * 1.5 - self.elipse_width // 2,
                                      self.radius * self.scale_rate * 2.075 - self.elipse_height // 2,
                                      150, 60)
        
        # Creating the ellipse surface
        change_surface = pygame.Surface((self.elipse_width, self.elipse_height), pygame.SRCALPHA, 32)
        
        pygame.draw.ellipse(change_surface, self.elipse_color, pygame.Rect(self.elipse_width // 4, self.elipse_height // 4, self.elipse_width // 2, self.elipse_height // 2))
    
        damage_text = self.font.render(str(self.current_menu_page + 1) + " / " + str(len(self.menu_pages)), True, self.text_color)
        change_surface.blit(damage_text, (self.elipse_width // 2 - damage_text.get_width() // 2,
                                          self.elipse_height // 2 - damage_text.get_height() // 2))
        
        # Drawing arrows and updating their position
        self.page_arrow_left_rect = change_surface.blit(self.arrow_left, (self.elipse_width // 6, self.elipse_height // 2 - self.arrow_left.get_height() // 2))
        self.page_arrow_left_rect.x += change_rect.x + self.x - (self.radius * 1.5 * self.scale_rate)
        self.page_arrow_left_rect.y += change_rect.y + self.y - (self.radius * 1.5 * self.scale_rate)
        
        self.page_arrow_right_rect = change_surface.blit(self.arrow_right, (self.elipse_width - self.arrow_right.get_width() - self.elipse_width // 6, self.elipse_height // 2 - self.arrow_right.get_height() // 2))
        self.page_arrow_right_rect.x += change_rect.x + self.x - (self.radius * 1.5 * self.scale_rate)
        self.page_arrow_right_rect.y += change_rect.y + self.y - (self.radius * 1.5 * self.scale_rate)
        
        # Blitting the ellipse on the tower_menu_surface
        tower_menu_surface.blit(change_surface, (change_rect.x, change_rect.y))
    
    def get_safe_positions(self, tower_menu_positions, screen):
        safe_positions = []

        for pos in Position:
            top_left_x = tower_menu_positions[pos.value][0] + self.x - (self.radius * 1.5 * self.scale_rate)
            top_left_y = tower_menu_positions[pos.value][1] + self.y - (self.radius * 1.5 * self.scale_rate)
            bottom_right_x = top_left_x + self.elipse_width
            bottom_right_y = top_left_y + self.elipse_height

            if (top_left_x >= 0 and bottom_right_x <= screen.get_width() * 0.85 and
                top_left_y >= 0 and bottom_right_y <= screen.get_height()):
                safe_positions.append(pos)

        return safe_positions

    
    def get_draw_ellipse_fuctions(self):
        
        return [self.draw_damage_dealt_ellipse,
                self.draw_upgrade_ellipse,
                self.draw_sell_ellipse,
                self.draw_target_mode_ellipse,
                self.draw_cooldown_ellipse,
                self.draw_damage_ellipse
                ]

    def draw_on_top(self, screen, delta_time):
        
        if self.selected:
            
            # Calculating ellipses positions
            tower_menu_positions = self.calculate_menu_positions()
            
            # Calculating positions where ellipses aren't off screen
            safe_positions = self.get_safe_positions(tower_menu_positions, screen)
            
            if not safe_positions:
                raise ValueError("No safe positions for ellipses! (Shouldn't happen, check the code!)")
            
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
            
            if Position.TOP in safe_positions:
                self.draw_menu_change_arrows(Position.TOP.value, self.menu_pages[self.current_menu_page])
            else:
                self.draw_menu_change_arrows(Position.BOTTOM.value, self.menu_pages[self.current_menu_page])
            
            # Drawing tower_menu_surface on the screen
            screen.blit(self.menu_pages[self.current_menu_page], (self.x - (self.radius * 1.5 * self.scale_rate), self.y - (self.radius * 1.5 * self.scale_rate)))
            
            # Drawing tower on top so it isn't under the tower menu
            self.draw(screen, delta_time) 


    def set_tower_target(self, target):
        self.tower_target = target

    def get_tower_target(self, enemies):

        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        if enemies_collision:

            match self.tower_target:
                case Target.FIRST:
                    
                    first_enemy = enemies_collision[0]

                    for enemy in enemies_collision:
                        if enemy.path_pos > first_enemy.path_pos:
                            first_enemy = enemy
                    
                    return first_enemy

                case Target.LAST:
                    
                    last_enemy = enemies_collision[0]

                    for enemy in enemies_collision:
                        if enemy.path_pos < last_enemy.path_pos:
                            last_enemy = enemy

                    return last_enemy

                case Target.MOST_HEALTH:
                    
                    most_hp_enemy = enemies_collision[0]

                    for enemy in enemies_collision:
                        if enemy.health > most_hp_enemy.health:
                            most_hp_enemy = enemy
                    
                    return most_hp_enemy

                case Target.LEAST_HEALTH:
                    
                    least_hp_enemy = enemies_collision[0]

                    for enemy in enemies_collision:
                        if enemy.health < least_hp_enemy.health:
                            least_hp_enemy = enemy

                    return least_hp_enemy

                case Target.ALL:
                    return enemies_collision
                case Target.NOT_SET:
                    raise ValueError("Tower target not set!")
                
        return []

    def manage_tower_action(self, clicked_position, money, text_alerts):
        if self.sell_icon_rect.collidepoint(clicked_position):
            self.sell_sound.play()
            return self.price

        if self.level <= 3 and self.upgrade_icon_rect.collidepoint(clicked_position):
            if money - self.price < 0:
                text_alerts.add(TextAlert("Not enough money!", 1000, (255, 0, 0)))
                return 0
            
            self.level += 1
            self.damage *= 1.2
            self.radius *= 1.1
            self.cooldown *= 0.9

            self.upgrade_sound.play()

            return -self.price
        return 0

    
    def manage_tower_target_mode(self, clicked_position):
        
        if self.arrow_right_rect.collidepoint(clicked_position):
            self.current_target_mode = (self.current_target_mode + 1) % len(self.target_modes)
            self.tower_target = self.target_modes[self.current_target_mode]
            return True
        
        if self.arrow_left_rect.collidepoint(clicked_position):
            if self.current_target_mode == 0:
                self.current_target_mode = len(self.target_modes) - 1
            else:
                self.current_target_mode -= 1

            self.tower_target = self.target_modes[self.current_target_mode]
            return True
        
        return False
    
    def manage_tower_menu_page(self, clicked_position):
        
        if self.page_arrow_left_rect.collidepoint(clicked_position):
            if self.current_menu_page > 0:
                self.current_menu_page -= 1
            return True
        
        if self.page_arrow_right_rect.collidepoint(clicked_position):
            if self.current_menu_page < len(self.menu_pages) - 1:
                self.current_menu_page += 1
            return True
        
        return False

    def select_tower(self, X, Y):
        if abs(X-self.x) < self.image.get_width()//2:
            if abs(Y-self.y) < self.image.get_height()//2:
                self.selected = True
                
                return True
        return False
    