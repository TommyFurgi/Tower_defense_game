import pygame
from towers.tower import Tower
from effects.effect_type import EffectType
from effects.slow_down_effect import SlowDownEffect
from source_manager import SourceManager
from towers.target import Target
from math import sqrt


class MagicTower(Tower):
    def __init__(self, x, y, x_scale_rate, y_scale_rate):
        Tower.__init__(self, x, y, x_scale_rate, y_scale_rate)

        self.tower_img = SourceManager.get_image("magic_tower").convert_alpha()
        self.tower_img_transformed = pygame.transform.scale(self.tower_img, (150 * x_scale_rate, 150 * y_scale_rate))
        
        self.damage = 15
        self.radius_start = 120
        self.radius = self.radius_start * sqrt((x_scale_rate**2 + y_scale_rate**2)/2)
        self.cooldown = 1000
        self.price = 300
        
        self.applied_effect = EffectType.SLOWDOWN
        self.effect_strength = 0.85
        self.effect_duration = 3
        
        self.cooldown_timer = self.cooldown

        self.damage_flash_duration = 200
        self.damage_flash_timer = 0
        self.damage_color = (224, 237, 111, 100)

        self.set_tower_target(Target.ALL)

        self.target_modes = [Target.ALL]
        self.shot_sound = SourceManager.get_sound("magic_shot")



    def find_targets(self, enemies, delta_time):
        
        if self.cooldown_timer <= 0:
                
            enemies_collision = self.get_tower_target(enemies)
                
            if enemies_collision:
                self.shot_sound.play()
                self.cooldown_timer = self.cooldown
                #self.damage_flash_timer = pygame.time.get_ticks()
                self.damage_flash_timer = self.damage_flash_duration # resetting flash damage timer

                for enemy in enemies_collision:
                    actual_damage = enemy.lose_hp(self.damage)
                    self.damage_dealt += actual_damage
                    enemy.add_effect(SlowDownEffect(self.effect_strength, self.effect_duration))
        else:
            self.cooldown_timer -= delta_time
        

    def draw(self, screen, delta_time):
        super().draw(screen, delta_time)
        
        if self.damage_flash_timer > 0:
            self.draw_demage_circle(screen)
            self.damage_flash_timer -= delta_time
            

    
    def draw_demage_circle(self, screen):
        scale_rate = 1.2

        surface = pygame.Surface((self.radius * 2 * scale_rate, self.radius * 2 * scale_rate), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.damage_color, (self.radius*scale_rate, self.radius*scale_rate), self.radius*scale_rate, 0)

        screen.blit(surface, (self.x - self.radius * scale_rate, self.y - self.radius * scale_rate))
        

    def update(self, game_pasue, enemies, screen, delta_time):
        if not game_pasue:
            self.find_targets(enemies, delta_time)
        
        
    
        
        
        