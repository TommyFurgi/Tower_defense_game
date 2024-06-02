import pygame
from abc import ABC
from towers.target import Target
from towers.tower_menu import TowerMenu
from source_manager import SourceManager
from text_alert import TextAlert


class Tower(pygame.sprite.Sprite, ABC): 
    def __init__(self, x, y, x_scale_rate, y_scale_rate): 
        pygame.sprite.Sprite.__init__(self)
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.start_x = x / x_scale_rate 
        self.start_y = y / y_scale_rate

        self.x = x
        self.y = y
        
        self.rect = pygame.Rect(x, y, 50 * x_scale_rate, 50 * y_scale_rate) 
        self.rect.center = (x, y) 
        
        self.level = 1
        self.selected = False

        self.damage_dealt = 0

        self.tower_target = Target.NOT_SET
        self.target_modes = []
        self.current_target_mode = 0

        self.time_from_last_shot = pygame.time.get_ticks()
        
        self.sell_sound = SourceManager.get_sound("selling")
        self.upgrade_sound = SourceManager.get_sound("upgrade")
        
        self.tower_menu = TowerMenu(self.x, self.y, self.x_scale_rate, self.y_scale_rate)
        

    def draw(self, screen, delta_time):
        screen.blit(self.tower_img_transformed, (self.x - self.tower_img_transformed.get_width() // 2, self.y - self.tower_img_transformed.get_height() // 2))  


    def draw_on_top(self, screen, delta_time):
        if self.selected:
            
            tower_parameters = {"level" : self.level, "damage" : self.damage, "radius" : self.radius, "cooldown" : self.cooldown,
                                "price" : self.price, "damage_dealt" : self.damage_dealt, "tower_target" : self.tower_target,
                                "radius" : self.radius}
            
            # Drawing tower menu
            self.tower_menu.draw(screen, tower_parameters)
                        
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
    
    
    def select_tower(self, X, Y):
        if abs(X-self.x) < self.tower_img_transformed.get_width()//2:
            if abs(Y-self.y) < self.tower_img_transformed.get_height()//2:
                self.selected = True
                
                return True
        return False

    
    def upgrade_tower(self, mouse_pos, money, text_alerts):
        if self.tower_menu.upgrade_pressed(mouse_pos):
            
            self.upgrade_sound.play()
            
            if self.level <= 3 and money - self.price < 0:
                text_alerts.add(TextAlert("Not enough money!", 1000, (255, 0, 0)))
                return -1
            else:
                self.level += 1
                self.damage *= 1.2
                self.radius *= 1.1
                self.radius_start *= 1.1
                self.cooldown *= 0.9
                
                self.tower_menu.set_radius(self.radius)

                self.upgrade_sound.play()

                return self.price
        return -1
    
    def sell_tower(self, mouse_pos):
        if self.tower_menu.sell_pressed(mouse_pos):
            
            self.sell_sound.play()
            
            return self.price
        
        return -1
        
    def change_tower_target_mode(self, clicked_position):
        if self.tower_menu.taget_mode_right_arrow_pressed(clicked_position):
            self.current_target_mode = (self.current_target_mode + 1) % len(self.target_modes)
            self.tower_target = self.target_modes[self.current_target_mode]
            return True
        
        if self.tower_menu.taget_mode_left_arrow_pressed(clicked_position):
            if self.current_target_mode == 0:
                self.current_target_mode = len(self.target_modes) - 1
            else:
                self.current_target_mode -= 1

            self.tower_target = self.target_modes[self.current_target_mode]
            return True
        
        return False

    def scale_parameters(self, x_scale_rate, y_scale_rate):
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.x = self.start_x * x_scale_rate
        self.y = self.start_y * y_scale_rate
        
        self.tower_menu.scale_parameters(self.x, self.y, x_scale_rate, y_scale_rate)
        
        self.rect = pygame.Rect(self.x, self.y, 50 * x_scale_rate, 50 * y_scale_rate) 
        self.rect.center = (self.x, self.y) 