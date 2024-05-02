import pygame, math
from directions import Direction
from abc import ABC, abstractmethod
from effects.effect_type import EffectType

class Enemy(pygame.sprite.Sprite, ABC):
    
    def __init__(self, images_filename):

        pygame.sprite.Sprite.__init__(self)
        
        
        self.reached_last_point = False
        
        self.effects = set()
        
        self.damage_animation_duration = 0.5
        self.damage_animation_timer = 0

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

        screen.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height() ))
        self.draw_health_bar(screen)
        
    def draw_on_top(self, screen):
        pass

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
    
    def update(self, game_pause):
        if not game_pause:
            self.move()
            self.handle_effects()
            
        #self.draw()

    # Damage
    def lose_hp(self, hp_lost):
        self.health -= hp_lost
        
    def to_delete(self):
        return self.reached_last_point
    
    def is_killed(self):
        if self.health <= 0:
            return True, self.reward
        
        return False, None
    
    def get_position(self):
        return self.x, self.y
        