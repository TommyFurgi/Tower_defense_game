import pygame
from towers.tower import Tower
from towers.bullet import Bullet
from effects.effect_type import EffectType
from effects.poison_effect import PoisonEffect
from resource_manager import ResourceManager
from towers.target import Target
from math import sqrt


class ArcherTower(Tower):
    """
    A variant of a Tower that shoots small bullets
    and applies Poison effect. 
    """
    def __init__(self, x, y, x_scale_rate, y_scale_rate):        
        Tower.__init__(self, x, y, x_scale_rate, y_scale_rate)

        self.tower_img = ResourceManager.get_image("archer_tower").convert_alpha()
        self.tower_img_transformed = pygame.transform.scale(self.tower_img, (150 * x_scale_rate, 150 * y_scale_rate))
        
        self.damage = 50
        self.radius_start = 150
        self.radius = self.radius_start * sqrt((x_scale_rate**2 + y_scale_rate**2)/2)
        self.cooldown = 700
        self.price = 400   
        
        self.applied_effect = EffectType.POISON
        self.effect_strength = 10
        self.effect_duration = 3
        
        self.cooldown_timer = self.cooldown

        self.bullets = pygame.sprite.Group()
        self.tower_target = Target.FIRST

        self.target_modes = [Target.FIRST, Target.LAST, Target.LEAST_HEALTH, Target.MOST_HEALTH]
        self.shot_sound = ResourceManager.get_sound("arrow_shot")


    def find_targets(self, enemies, delta_time):
        """
        This function finds enemies which are in range of a tower
        then sends a bullet to them
        """
        if self.cooldown_timer <= 0:
            
            enemy = self.get_tower_target(enemies)
            
            if enemy:
                self.shot_sound.play()
                self.cooldown_timer = self.cooldown
                enemy_x, enemy_y = enemy.get_position()
                self.bullets.add(Bullet(15, self.x, self.y - 70 * self.y_scale_rate, enemy_x, enemy_y - 60 * self.y_scale_rate, enemy, self.x_scale_rate, self.y_scale_rate))
            
        else:
            self.cooldown_timer -= delta_time
 
 
    def update(self, game_pasue, enemies, screen, delta_time):
        """
        Function called every frame, triggers find_targets, then checks
        if each bullet hit it's target and eventually deals a damage to
        an enemy and applies PoisonEffect to them.  
        """        
        if not game_pasue:
            self.find_targets(enemies, delta_time)

        self.bullets.update(game_pasue, screen)

        bullets_to_remove = []
        
        for bullet in self.bullets:
            enemy_hitted = bullet.hit()
            if enemy_hitted:
                if(enemy_hitted.add_effect(PoisonEffect(self.effect_strength, self.effect_duration))): # Returns true if the effect was added, false if enemy is resistant to the effect
                    self.damage_dealt += 3 * 10
                actual_damage = enemy_hitted.lose_hp(self.damage)
                self.damage_dealt += actual_damage
                
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)


    def scale_parameters(self, x_scale_rate, y_scale_rate):
        """
        Scales necessary parameters. Triggered when users
        resizes game window.
        """
        super().scale_parameters(x_scale_rate, y_scale_rate)

        for bullet in self.bullets:
            bullet.scale_parameters(x_scale_rate, y_scale_rate)

        
    
        
        
        