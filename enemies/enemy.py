import pygame, math
from directions import Direction
from abc import ABC
from effects.effect_type import EffectType


class Enemy(pygame.sprite.Sprite, ABC):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.reached_last_point = False
        
        self.effects = dict()
        self.prepare_effects_dict()
        
        self.poison_resistance = 0.25 # 0.25%

        self.damage_flash_color = (255, 255, 255)
        self.damage_flash_duration = 100 # ms
        self.damage_flash_timer = 0
        
        self.colors = set()       
        
        self.hp_font = pygame.font.Font(None, 20) 


    def draw_health_bar(self, screen):
        length = 80
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(screen, (255,0,0), (self.x-42, self.y - 130, length, 10), 0)
        pygame.draw.rect(screen, (0, 255, 0), (self.x-42, self.y - 130, health_bar, 10), 0)

        # Wyświetlanie ilości punktów życia na pasku
        text = self.hp_font.render(f"{self.health}/{self.max_health}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y - 125))
        screen.blit(text, text_rect)


    def add_color(self, color):
        self.colors.add(color)
    

    def remove_color(self, color):
        if color in self.colors:
            self.colors.remove(color)


    def enemy_animation(self):
        match self.direction:
            case Direction.UP:
                self.img = self.imgs_up[self.animation_count//10]
            case Direction.DOWN:
                self.img = self.imgs_down[self.animation_count//10]
            case Direction.RIGHT:
                self.img = self.imgs_right[self.animation_count//10]
            case Direction.LEFT:
                self.img = self.imgs_left[self.animation_count//10] 


    def draw(self, screen):
        self.enemy_animation()
    
        if pygame.time.get_ticks() - self.damage_flash_timer < self.damage_flash_duration:
            img_copy = self.img.copy() # Creates a copy of img (Could be inefficient, but you can't directly change pixels on img)
            img_copy.fill(self.damage_flash_color, special_flags = pygame.BLEND_RGB_MAX) # Fills non transparent pixels of copied image with given color
            self.img = img_copy
            #screen.blit(img_copy, (self.x - self.img.get_width()/2, self.y - self.img.get_height())) 
            
        if len(self.colors) > 0:
            img_copy = self.img.copy()
            for color in self.colors:
                img_copy.fill(color, special_flags = pygame.BLEND_RGB_ADD)
            self.img = img_copy
        
        screen.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height())) # Draws sprite in normal color
        
        self.draw_health_bar(screen)



    def move(self):
        self.animation_count += 1
        if self.animation_count >= len(self.imgs_up) * 10:
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 < len(self.path):
            x2, y2 = self.path[self.path_pos+1]
        else:
            self.reached_last_point = True
            return
        
        if self.x > 1350:
            self.reached_last_point = True
            return

        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)
        dirn = (dirn[0] * self.speed, dirn[1] * self.speed)


        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.x = move_x
        self.y = move_y
        
        self.rect.center = (move_x, move_y)

        # Go to next point
        if dirn[0] >= 0: # moving right
            if dirn[1] >= 0: # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else: # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y <= y2:
                    self.path_pos += 1
 
        
        # Setting direction
        self.direction = Direction.set_direction(dirn)


    def update(self, game_pause, enemies):
        if not game_pause:
            self.move()
            self.remove_inactive_effects()
            self.handle_poison_effect()
            
    # Damage
    def lose_hp(self, hp_lost, color = (255, 255, 255)):
        self.health -= hp_lost
        
        if pygame.time.get_ticks() - self.damage_flash_timer > self.damage_flash_duration:
            self.damage_flash_color = color
            self.damage_flash_timer = pygame.time.get_ticks()
        

    def to_delete(self):
        return self.reached_last_point
    

    def is_killed(self):
        if self.health <= 0:
            return True, self.reward
        
        return False, None
    

    def get_position(self):
        return self.x, self.y
        

    def pause_effects(self):
        for effect in EffectType:
            if self.effects[effect]:
                self.effects[effect].pause_effect()

    def unpause_effects(self):
        for effect in EffectType:
            if self.effects[effect]:
                self.effects[effect].pause_effect()


    def prepare_effects_dict(self):
        for effect in EffectType:
            self.effects[effect] = None


    def add_effect(self, new_effect):
        # Enemy should only have one effect of given type at a time 
        match new_effect.get_effect_type():

            case EffectType.POISON:
                
                self.remove_effect(EffectType.POISON)
                self.effects[EffectType.POISON] = new_effect

            case EffectType.BOOST:
                
                #Slowdown cancels boost
                if self.effects[EffectType.SLOWDOWN]:
                    return

                self.remove_effect(EffectType.BOOST)
                self.effects[EffectType.BOOST] = new_effect
                self.handle_boost_effect()

            case EffectType.SLOWDOWN:
                
                #Slowdown cancels boost
                if self.effects[EffectType.BOOST]:
                    self.remove_effect(EffectType.BOOST)

                self.remove_effect(EffectType.SLOWDOWN)
                self.effects[EffectType.SLOWDOWN] = new_effect
                self.handle_slow_down_effect()
    

    def remove_effect(self, effect_type):
            
            if self.effects[effect_type]:
                _, color = self.effects[effect_type].get_values()
                self.remove_color(color)
                self.effects[effect_type] = None

                if effect_type == EffectType.BOOST or effect_type == EffectType.SLOWDOWN:
                    self.speed = self.max_speed
                
                self.effects[effect_type] = None


    def remove_inactive_effects(self):
        for effect in EffectType:
            if self.effects[effect]:
                if not self.effects[effect].is_active():
                    self.remove_effect(effect)


    def handle_poison_effect(self):
        if self.effects[EffectType.POISON]:
            value, color = self.effects[EffectType.POISON].update()
            
            if value and color:
                self.lose_hp(value * (1 - self.poison_resistance))
                if color not in self.colors:
                    self.add_color(color)


    def handle_boost_effect(self):
        if self.effects[EffectType.BOOST]:
            value, color = self.effects[EffectType.BOOST].get_values()

            self.speed = value * self.max_speed
            self.add_color(color)


    def handle_slow_down_effect(self):
        if self.effects[EffectType.SLOWDOWN]:
            value, color = self.effects[EffectType.SLOWDOWN].get_values()

            self.speed = value * self.max_speed
            self.add_color(color)