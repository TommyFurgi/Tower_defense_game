import pygame
from towers.tower import Tower
from effects.slow_down_effect import SlowDownEffect
from source_manager import SourceManager
from towers.target import Target


class MagicTower(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y)

        self.image = SourceManager.get_image("magic_tower").convert_alpha()

        self.image = pygame.transform.scale(self.image, (150, 150))
        
        self.rect = pygame.Rect(x, y, 50, 50) 
        self.rect.center = (x, y) 
        
        self.damage = 75
        self.radius = 120
        self.cooldown = 1000
        self.price = 300
        
        self.cooldown_timer = self.cooldown

        self.damage_flash_duration = 200
        self.damage_flash_timer = 0
        self.damage_color = (224, 237, 111, 100)

        self.update_tower_feature_rect()

        self.set_tower_target(Target.ALL)

        self.target_modes = [Target.ALL]



    def find_targets(self, enemies, delta_time):
        
        if self.cooldown_timer <= 0:
                
            enemies_collision = self.get_tower_target(enemies)
                
            if enemies_collision:
                
                self.cooldown_timer = self.cooldown
                #self.damage_flash_timer = pygame.time.get_ticks()
                self.damage_flash_timer = self.damage_flash_duration # resetting flash damage timer

                for enemy in enemies_collision:
                    actual_damage = enemy.lose_hp(self.damage)
                    self.damage_dealt += actual_damage
                    enemy.add_effect(SlowDownEffect(0.85, 3))
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
        
        
    
        
        
        