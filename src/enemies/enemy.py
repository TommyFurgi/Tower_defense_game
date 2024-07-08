import pygame, math
from directions import Direction
from abc import ABC
from effects.effect_type import EffectType
from resource_manager import ResourceManager

class Enemy(pygame.sprite.Sprite, ABC):
    '''
    An abstract base class for enemies, responsible for managing enemy behavior, including movement, 
    effects, and rendering. Inherits from `pygame.sprite.Sprite` and `ABC` (Abstract Base Class).
    ''' 
    def __init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff, path_name):
        '''
        Initializes the Enemy instance with scaling factors and prepares its starting parameters.
        
        Args:
            x_scale_rate (float): The scaling factor for the x-axis.
            y_scale_rate (float): The scaling factor for the y-axis.
            x_scale_diff (float): The scaling difference for the x-axis.
            y_scale_diff (float): The scaling difference for the y-axis.
        '''
        pygame.sprite.Sprite.__init__(self)
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.x_scale_diff = x_scale_diff
        self.y_scale_diff = y_scale_diff

        self.path = ResourceManager.get_path(path_name)
                
        # starting point
        self.x = self.path[0][0] 
        self.y = self.path[0][1] 

        self.reached_last_point = False
        self.rect = pygame.Rect(self.x, self.y, 64, 64) # Required in order for collisions to work
        self.direction = Direction.RIGHT
        self.path_pos = 0

        self.effects = dict()
        self.prepare_effects_dict()
        
        self.effects_resistance = dict() # dictionary of effects that enemy is resistant to
        self.prepare_effects_resistance_dict()
        
        self.poison_resistance = 0.25 # 0.25%

        self.damage_flash_color = (255, 255, 255)
        self.damage_flash_duration = 100 # ms
        self.damage_flash_timer = 0 # ms
        
        self.colors = set()       
        self.hp_font = pygame.font.Font(None, 20) 

    def draw_health_bar(self, screen):
        '''
        Draws the health bar of the enemy above its current position on the screen.
        
        Args:
            screen (pygame.Surface): The surface on which the health bar will be drawn.
        '''
        length = 80
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(screen, (255,0,0), (self.x - 42 * self.x_scale_rate, self.y - 130 * self.y_scale_rate, length * self.x_scale_rate, 10 * self.y_scale_rate), 0)
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 42 * self.x_scale_rate, self.y - 130 * self.y_scale_rate, health_bar * self.x_scale_rate, 10 * self.y_scale_rate), 0)

        # Wyświetlanie ilości punktów życia na pasku
        text = self.hp_font.render(f"{int(self.health)}/{self.max_health}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y - 125 * self.y_scale_rate))
        screen.blit(text, text_rect)

    def add_color(self, color):
        '''
        Adds a color to the enemy, used to visually represent the effects applied to it.
        
        Args:
            color (tuple): The color to add, typically used for effects.
        '''
        self.colors.add(color)
    
    def remove_color(self, color):
        '''
        Removes a color from the enemy.
        
        Args:
            color (tuple): The color to remove.
        '''
        if color in self.colors:
            self.colors.remove(color)

    def enemy_animation(self):
        '''
        Sets the image for the enemy based on its current direction, to be used for rendering.
        '''
        match self.direction:
            case Direction.UP:
                self.img = self.imgs_up[self.animation_count//10]
            case Direction.DOWN:
                self.img = self.imgs_down[self.animation_count//10]
            case Direction.RIGHT:
                self.img = self.imgs_right[self.animation_count//10]
            case Direction.LEFT:
                self.img = self.imgs_left[self.animation_count//10] 

    def draw(self, screen, delta_time):
        '''
        Sets the image for the enemy based on its current direction, to be used for rendering.
        '''
        self.enemy_animation()
    
        if self.damage_flash_timer > 0:
            
            img_copy = self.img.copy() # Creates a copy of img (Could be inefficient, but you can't directly change pixels on img)
            img_copy.fill(self.damage_flash_color, special_flags = pygame.BLEND_RGB_MAX) # Fills non transparent pixels of copied image with given color
            self.img = img_copy
            
            self.damage_flash_timer -= delta_time
            
            
        if len(self.colors) > 0:
            img_copy = self.img.copy()
            for color in self.colors:
                img_copy.fill(color, special_flags = pygame.BLEND_RGB_ADD)
            self.img = img_copy
        
        screen.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height())) # Draws sprite in normal color
        
        self.draw_health_bar(screen)

    def move(self):
        '''
        Moves the enemy along its path towards the next waypoint. Updates the enemy's position and sets the direction.
        '''
        self.animation_count += 1
        if self.animation_count >= len(self.imgs_up) * 10:
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 < len(self.path):
            x2, y2 = self.path[self.path_pos+1]
        else:
            self.reached_last_point = True
            return
            
        if self.x > 1350 * self.x_scale_rate:
            self.reached_last_point = True
            return

        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)
        dirn = (dirn[0] * self.speed, dirn[1] * self.speed)


        move_x, move_y = ((self.x + dirn[0] * self.x_scale_diff), (self.y + dirn[1] * self.y_scale_diff))
        self.x = move_x
        self.y = move_y
            
        self.rect.center = (move_x, move_y)

        # Go to next point
        if dirn[0] >= 0: # moving right
            if dirn[1] >= 0: # moving down
                if self.x >= x2 * self.x_scale_rate and self.y >= y2 * self.y_scale_rate:
                    self.path_pos += 1
            else:
                if self.x >= x2 * self.x_scale_rate and self.y <= y2 * self.y_scale_rate:
                    self.path_pos += 1
        else: # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 * self.x_scale_rate and self.y >= y2 * self.y_scale_rate:
                    self.path_pos += 1
            else:
                if self.x <= x2 * self.x_scale_rate and self.y <= y2 * self.y_scale_rate:
                    self.path_pos += 1
            
        # Setting direction
        self.direction = Direction.set_direction(dirn)

    def update(self, game_pause, enemies):
        '''
        Updates the enemy's state based on the game's pause status.
        
        Args:
            game_pause (bool): Flag indicating whether the game is paused.
            enemies (set): List of all enemies in the game.
        '''
        if not game_pause:
            self.move()
            self.remove_inactive_effects()
            self.handle_poison_effect()
            
    # Damage
    def lose_hp(self, hp_lost, color = (255, 255, 255)):
        '''
        Reduces the enemy's health points based on the damage received.
        
        Args:
            hp_lost (float): Amount of health points to deduct.
            color (tuple, optional): Color to flash when taking damage. Defaults to (255, 255, 255).
        
        Returns:
            float: Actual amount of health points deducted.
        '''
        if self.health < hp_lost:
            actual_damage = self.health
            self.health = 0
        else:
            actual_damage = hp_lost
            self.health -= hp_lost
        
        if self.damage_flash_timer <= 0:
            self.damage_flash_color = color
            self.damage_flash_timer = self.damage_flash_duration
            
        return actual_damage
        
    def to_delete(self):
        '''
        Determines whether the enemy has reached the last point in its path.
        
        Returns:
            bool: True if the enemy has reached the last point, False otherwise.
        '''
        return self.reached_last_point
    
    def is_killed(self):
        '''
        Checks if the enemy is killed (health is zero or below).
        
        Returns:
            tuple: A tuple where the first element is a boolean indicating if the enemy is killed,
                   and the second element is the reward (currently None).
        '''
        return self.health <= 0, self.reward
    
    def get_position(self):
        '''
        Retrieves the current position of the enemy.
        
        Returns:
            tuple: Current x and y coordinates of the enemy.
        '''
        return self.x, self.y
        
    def pause_effects(self):
        '''
        Pauses all active effects on the enemy.
        '''
        for effect in EffectType:
            if self.effects[effect]:
                self.effects[effect].pause_effect()

    def unpause_effects(self):
        '''
        Unpauses all active effects on the enemy.
        '''
        for effect in EffectType:
            if self.effects[effect]:
                self.effects[effect].pause_effect()

    def prepare_effects_dict(self):
        '''
        Initializes the effects dictionary with None values for each effect type.
        '''
        for effect in EffectType:
            self.effects[effect] = None

    def prepare_effects_resistance_dict(self):
        '''
        Initializes the effects resistance dictionary with False values for each effect type.
        '''
        for effect in EffectType:
            self.effects_resistance[effect] = False

    def is_resistant(self, effect_type):
        '''
        Checks if the enemy is resistant to a specific type of effect.
        
        Args:
            effect_type (EffectType): The type of effect to check resistance against.
        
        Returns:
            bool: True if the enemy is resistant to the effect type, False otherwise.
        '''
        return self.effects_resistance[effect_type]
    
    def add_effect(self, new_effect):
        '''
        Adds a new effect to the enemy if it's not already resistant to it or if the new effect supersedes existing effects.
        
        Args:
            new_effect (Effect): The new effect instance to add.
        
        Returns:
            bool: True if the effect was successfully added, False otherwise.
        '''
        # Enemy should only have one effect of given type at a time 
        match new_effect.get_effect_type():

            case EffectType.POISON if not self.is_resistant(EffectType.POISON):
                
                self.remove_effect(EffectType.POISON)
                self.effects[EffectType.POISON] = new_effect
                return True

            case EffectType.BOOST if not self.is_resistant(EffectType.BOOST):
                
                #Slowdown cancels boost
                if self.effects[EffectType.SLOWDOWN]:
                    return

                self.remove_effect(EffectType.BOOST)
                self.effects[EffectType.BOOST] = new_effect
                self.handle_boost_effect()
                return True

            case EffectType.SLOWDOWN if not self.is_resistant(EffectType.SLOWDOWN):
                
                #Slowdown cancels boost
                if self.effects[EffectType.BOOST]:
                    self.remove_effect(EffectType.BOOST)

                self.remove_effect(EffectType.SLOWDOWN)
                self.effects[EffectType.SLOWDOWN] = new_effect
                self.handle_slow_down_effect()
                return True
    
        return False
    
    def remove_effect(self, effect_type):
        '''
        Removes an active effect from the enemy.
        
        Args:
            effect_type (EffectType): The type of effect to remove.
        '''
        if self.effects[effect_type]:
            _, color = self.effects[effect_type].get_values()
            self.remove_color(color)
            self.effects[effect_type] = None

            if effect_type == EffectType.BOOST or effect_type == EffectType.SLOWDOWN:
                self.speed = self.max_speed
            
            self.effects[effect_type] = None

    def remove_inactive_effects(self):
        '''
        Removes all inactive effects from the enemy.
        '''
        for effect in EffectType:
            if self.effects[effect]:
                if not self.effects[effect].is_active():
                    self.remove_effect(effect)

    def handle_poison_effect(self):
        '''
        Updates and handles the poison effect on the enemy.
        '''
        if self.effects[EffectType.POISON]:
            value, color = self.effects[EffectType.POISON].update()
            
            if value and color:
                self.lose_hp(value * (1 - self.poison_resistance))
                if color not in self.colors:
                    self.add_color(color)

    def handle_boost_effect(self):
        '''
        Applies and handles the boost effect on the enemy.
        '''
        if self.effects[EffectType.BOOST]:
            value, color = self.effects[EffectType.BOOST].get_values()

            self.speed = value * self.max_speed
            self.add_color(color)

    def handle_slow_down_effect(self):
        '''
        Applies and handles the slowdown effect on the enemy.
        '''
        if self.effects[EffectType.SLOWDOWN]:
            value, color = self.effects[EffectType.SLOWDOWN].get_values()

            self.speed = value * self.max_speed
            self.add_color(color)

    def scale_parameters(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff, initialize_enemy = False):
        '''
        Scales the parameters of the enemy based on given scaling factors and differences.
        
        Args:
            x_scale_rate (float): The scaling factor for the x-axis.
            y_scale_rate (float): The scaling factor for the y-axis.
            x_scale_diff (float): The scaling difference for the x-axis.
            y_scale_diff (float): The scaling difference for the y-axis.
            initialize_enemy (bool): The flag indicating whether the function is called during initialization
        '''
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.x_scale_diff = x_scale_diff
        self.y_scale_diff = y_scale_diff

        if initialize_enemy:
            self.x *= x_scale_rate
            self.y *= y_scale_rate
        else:
            self.x *= x_scale_diff
            self.y *= y_scale_diff

        self.rect = pygame.Rect(self.x, self.y, 64 * x_scale_rate, 64 * y_scale_rate)
        self.hp_font = pygame.font.Font(None, int(20 * x_scale_rate)) 
    
