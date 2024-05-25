import pygame
from abc import ABC
from text_alert import TextAlert
from towers.target import Target
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


    def draw(self, screen, delta_time):
        screen.blit(self.image, (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))


    def draw_tower_menu(self, screen):

        self.draw_stats(screen)
        self.draw_target_mode_selection(screen)

        upgrade_rect = pygame.Rect(self.x + self.radius * 0.5, self.y + self.radius * 0.3 - 5, 150, 60)
        pygame.draw.ellipse(screen, (133, 98, 42), upgrade_rect)

        screen.blit(self.sell_icon, (self.x + self.radius * 0.5, self.y + self.radius * 0.3))

        text = self.font.render("Price: " + str(self.price), True, (255, 255, 255))
        screen.blit(text, (self.x + self.radius * 0.5 + 60, self.y + self.radius * 0.3 + 15))

        if self.level <= 3:
            upgrade_rect = pygame.Rect(self.x + self.radius * 0.5, self.y - self.radius * 0.3 - 5, 150, 60)
            pygame.draw.ellipse(screen, (133, 98, 42), upgrade_rect)

            screen.blit(self.upgrade_icon, (self.x + self.radius * 0.5, self.y - self.radius * 0.3))

            text = self.font.render("Price: " + str(self.price), True, (255, 255, 255))
            screen.blit(text, (self.x + self.radius * 0.5 + 60, self.y - self.radius * 0.3 + 10))

            level_text = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
            screen.blit(level_text, (self.x + self.radius * 0.5 + 60, self.y - self.radius * 0.3 + 30))

    def draw_stats(self, screen):

        damage_dealt_rect = pygame.Rect(self.x - 75, self.y - self.radius - 60, 150, 60)
        pygame.draw.ellipse(screen, (133, 98, 42), damage_dealt_rect)

        damage_dealt_info_text = self.font.render("Damage dealt:", True, (255, 255, 255))
        screen.blit(damage_dealt_info_text, (self.x - 50, self.y - self.radius - 45))

        
        damage_dealt_str = str(int(self.damage_dealt))
        if(int(self.damage_dealt) >= 1_000_000_000):
            damage_dealt_str = str(int(self.damage_dealt // 1_000_000_000)) + " B"
        # Possibly can add more checks for M, K, etc.

        offset_damage_dealt = 5 * (len(damage_dealt_str) - 1) if len(damage_dealt_str) > 1 else 0
        damage_dealt_amount_text = self.font.render(damage_dealt_str, True, (255, 255, 255))
        screen.blit(damage_dealt_amount_text, (self.x - offset_damage_dealt, self.y - self.radius - 25))
        
        damage_info_rect = pygame.Rect(self.x - self.radius * 0.5 - 150, self.y - self.radius * 0.3 - 5, 150, 60)
        pygame.draw.ellipse(screen, (133, 98, 42), damage_info_rect)

        damage_text = self.font.render("Damage: " + str(int(self.damage)), True, (255, 255, 255))
        screen.blit(damage_text, (self.x - self.radius * 0.5 - 120, self.y - self.radius * 0.3 + 15))

        cooldown_info_rect = pygame.Rect(self.x - self.radius * 0.5 - 150, self.y + self.radius * 0.3 - 5, 150, 60)
        pygame.draw.ellipse(screen, (133, 98, 42), cooldown_info_rect)

        damage_str = str(int(self.cooldown))
        offset_damage = 10 * (len(damage_str) - 3) if len(damage_str) > 3 else 0
        damage_text = self.font.render("Cooldown: " + damage_str, True, (255, 255, 255))
        screen.blit(damage_text, (self.x - self.radius * 0.5 - 130 - offset_damage , self.y + self.radius * 0.3 + 15))

    def draw_target_mode_selection(self, screen):

        target_mode_rect = pygame.Rect(self.x - 75, self.y + self.radius, 150, 60)
        pygame.draw.ellipse(screen, (133, 98, 42), target_mode_rect)        

        target_mode_info_text = self.font.render("Target mode:", True, (255, 255, 255))
        screen.blit(target_mode_info_text, (self.x - 45, self.y + self.radius + 15))

        target_mode_text = self.font.render(self.tower_target.value, True, (255, 255, 255))
        text_width = target_mode_text.get_width()
        text_x = self.x - text_width // 2
        screen.blit(target_mode_text, (text_x, self.y + self.radius + 35))

        screen.blit(self.arrow_right, (self.x + 60, self.y + self.radius + 15))
        screen.blit(self.arrow_left, (self.x - 90, self.y + self.radius + 15))

    def draw_on_top(self, screen, delta_time):
        if self.selected:
            self.draw_radius(screen)
            self.draw(screen, delta_time) # So the tower isn't drawn under the circle
            self.draw_tower_menu(screen)


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

            self.update_tower_feature_rect()
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


    def update_tower_feature_rect(self):
        self.sell_icon_rect = pygame.Rect(self.x + self.radius * 0.5, self.y + self.radius * 0.3, 50, 50) 
        self.upgrade_icon_rect = pygame.Rect(self.x + self.radius * 0.5, self.y - self.radius * 0.3, 50, 50) 
        self.arrow_right_rect = pygame.Rect(self.x + 60, self.y + self.radius + 15, 30, 30) 
        self.arrow_left_rect = pygame.Rect(self.x - 90, self.y + self.radius + 15, 30, 30)


    def draw_radius(self, screen):
        scale_rate = 1.3

        surface = pygame.Surface((self.radius * 2 * scale_rate, self.radius * 2 * scale_rate), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 255, 100), (self.radius*scale_rate, self.radius*scale_rate), self.radius*scale_rate, 0)

        screen.blit(surface, (self.x - self.radius * scale_rate, self.y - self.radius * scale_rate))


    def select_tower(self, X, Y):
        if abs(X-self.x) < self.image.get_width()//2:
            if abs(Y-self.y) < self.image.get_height()//2:
                self.selected = True
                
                return True
        return False
    