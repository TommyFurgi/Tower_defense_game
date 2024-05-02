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



    def find_targets(self, enemies):
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        if enemies_collision and pygame.time.get_ticks() - self.time_from_last_shot > self.cooldown:
            self.time_from_last_shot = pygame.time.get_ticks()
            # TODO: visual effect

            for enemy in enemies_collision:
                enemy.lose_hp(self.damage)
                enemy.add_effect(SlowDownEffect(0.85, 3))

    def update(self, game_pasue, enemies, screen):
        if not game_pasue:
            self.find_targets(enemies)

        self.draw(screen)
        
        
    
        
        
        