import pygame, math
from directions import Direction
from abc import ABC, abstractmethod
from effects.effect_type import EffectType

class Enemy(pygame.sprite.Sprite, ABC):
    
    def __init__(self, images_filename):

        pygame.sprite.Sprite.__init__(self)
        
        self.reached_last_point = False
        
        self.effects = set()
        
        self.damage_color = (255, 255, 255)
        
        self.damage_flash_duration = 100 # ms
        self.damage_flash_timer = 0

        self.load_images(images_filename)
        

    @abstractmethod
    def load_images(self, images_filename):
        pass


    def draw_health_bar(self, screen):
        length = 80
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(screen, (255,0,0), (self.x-42, self.y - 130, length, 10), 0)
        pygame.draw.rect(screen, (0, 255, 0), (self.x-42, self.y - 130, health_bar, 10), 0)

        # Wyświetlanie ilości punktów życia na pasku
        font = pygame.font.Font(None, 20)
        text = font.render(f"{self.health}/{self.max_health}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y - 125))
        screen.blit(text, text_rect)



    def draw(self, screen):

        match self.direction:
            case Direction.UP:
                self.img = self.imgs_up[self.animation_count//10]
            case Direction.DOWN:
                self.img = self.imgs_down[self.animation_count//10]
            case Direction.RIGHT:
                self.img = self.imgs_right[self.animation_count//10]
            case Direction.LEFT:
                self.img = self.imgs_left[self.animation_count//10]            

        if pygame.time.get_ticks() - self.damage_flash_timer < self.damage_flash_duration:
            self.draw_damage_flash(screen) # Draws sprite in white color
        else:
            screen.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height())) # Draws sprite in normal color
        
        self.draw_health_bar(screen)
        
    def draw_on_top(self, screen):
        pass

    def draw_damage_flash(self, screen):
        
        img_copy = self.img.convert(self.img) # Creates a copy of img (Could be inefficient, but you can't directly change pixels on img)
        img_copy.fill(self.damage_color, special_flags = pygame.BLEND_RGB_MAX) # Fills non transparent pixels of copied image with given color
        screen.blit(img_copy, (self.x - self.img.get_width()/2, self.y - self.img.get_height())) 

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

        # return True
    
    def add_effect(self, new_effect):
        
        # Enemy should only have one effect of given type at a time
        
        for effect in self.effects:
            
            if effect.get_effect_type() == new_effect.get_effect_type():
                self.effects.remove(effect)
                break
        
        self.effects.add(new_effect)    
    
    @abstractmethod
    def handle_effects(self):
        pass
    
    def update(self, game_pause, enemies):
        if not game_pause:
            self.move()
            self.handle_effects()
            
        #self.draw()

    # Damage
    def lose_hp(self, hp_lost, damage_color = (255, 255, 255)):
        self.health -= hp_lost
        self.damage_color = damage_color
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
        for effect in self.effects:
            effect.pause_effect()

    def unpause_effects(self):
        for effect in self.effects:
            effect.reset()