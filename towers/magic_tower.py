import pygame
from towers.tower import Tower
from menu import Menu
from effects.slow_down_effect import SlowDownEffect
from effects.effect_type import EffectType

class MagicTower(Tower):

    def __init__(self, x, y):
        
        Tower.__init__(self, x, y)

        self.image = pygame.image.load('assets/towers/magic_tower.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        
        self.rect = pygame.Rect(x, y, 50, 50) 
        self.rect.center = (x, y) 
        
        self.tower_imgs = [self.image]

        self.damage = 75
        self.radius = 120
        self.cooldown = 1000

        self.damage_flash_duration = 200 # ms
        self.damage_flash_timer = -float('inf')
        self.damage_color = (224, 237, 111, 100)



    def find_targets(self, enemies):
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        if enemies_collision and pygame.time.get_ticks() - self.time_from_last_shot > self.cooldown:
            self.time_from_last_shot = pygame.time.get_ticks()
            self.damage_flash_timer = pygame.time.get_ticks()

            for enemy in enemies_collision:
                enemy.lose_hp(self.damage)
                enemy.add_effect(SlowDownEffect(0.85, 3))
        
    def draw(self, screen):
        super().draw(screen)
        
        if pygame.time.get_ticks() - self.damage_flash_timer <= self.damage_flash_duration:
            self.draw_demage_circle(screen)

    
    def draw_demage_circle(self, screen):
        scale_rate = 1.2

        surface = pygame.Surface((self.radius * 2 * scale_rate, self.radius * 2 * scale_rate), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.damage_color, (self.radius*scale_rate, self.radius*scale_rate), self.radius*scale_rate, 0)

        screen.blit(surface, (self.x - self.radius * scale_rate, self.y - self.radius * scale_rate))
        

    def update(self, game_pasue, enemies, screen):
        if not game_pasue:
            self.find_targets(enemies)

        self.draw(screen)
        
        
    
        
        
        