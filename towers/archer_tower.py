import pygame
from towers.tower import Tower
from towers.bullet import Bullet
from effects.poison_effect import PoisonEffect
from source_manager import SourceManager


class ArcherTower(Tower):
    def __init__(self, x, y):        
        Tower.__init__(self, x, y)

        self.image = SourceManager.get_image("archer_tower").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        
        # This two attributes are required by pygame.sprite.Sprite in order for it to work properly
        self.rect = pygame.Rect(x, y, 50, 50) # Rect(left, top, width, height), but we want x,y to be the center of the tower
        self.rect.center = (x, y) # thus this line is needed
        
        self.damage = 100
        self.radius = 150
        self.cooldown = 700
        self.price = 400

        self.bullets = pygame.sprite.Group()
        self.update_tower_feature_rect()
    

    def find_targets(self, enemies):
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        if enemies_collision and pygame.time.get_ticks() - self.time_from_last_shot > self.cooldown:
            self.time_from_last_shot = pygame.time.get_ticks()
            enemy_x, enemy_y = enemies_collision[0].get_position()
            self.bullets.add(Bullet(15, self.x, self.y-70, enemy_x, enemy_y - 60, enemies_collision[0]))
            

    def update(self, game_pasue, enemies, screen):
        if not game_pasue:
            self.find_targets(enemies)

        self.bullets.update(game_pasue, screen)

        bullets_to_remove = []
        
        for bullet in self.bullets:
            enemy_hitted = bullet.hit()
            if enemy_hitted:
                enemy_hitted.add_effect(PoisonEffect(10, 3))
                self.damage_dealt += 3 * 10
                enemy_hitted.lose_hp(self.damage)
                self.damage_dealt += self.damage
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)



        
    
        
        
        