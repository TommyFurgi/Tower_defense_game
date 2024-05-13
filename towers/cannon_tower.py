import pygame
from towers.tower import Tower
from towers.bullet import Bullet

class CannonTower(Tower):
    
    def __init__(self, x, y):
        
        Tower.__init__(self, x, y)

        self.image = pygame.image.load('assets/towers/cannon_tower.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        
        self.rect = pygame.Rect(x, y, 50, 50) 
        self.rect.center = (x, y) 
        
        self.tower_imgs = [self.image]

        self.damage = 150
        self.radius = 100
        self.cooldown = 1700
        
        self.blast_radius = 70
        self.blast_damage = 40
        
        self.bullets = pygame.sprite.Group()
        
    def find_targets(self, enemies):
        
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        if enemies_collision and pygame.time.get_ticks() - self.time_from_last_shot > self.cooldown:
            self.time_from_last_shot = pygame.time.get_ticks()
            enemy_x, enemy_y = enemies_collision[0].get_position()
            self.bullets.add(Bullet(25, self.x, self.y-70, enemy_x, enemy_y - 60, enemies_collision[0]))

    def update(self, game_pasue, enemies, screen):
        if not game_pasue:
            self.find_targets(enemies)

        self.bullets.update(game_pasue, screen)

        bullets_to_remove = []
        
        for bullet in self.bullets:
            enemy_hitted = bullet.hit()
            if enemy_hitted:
                enemy_hitted.lose_hp(self.damage)    
                bullets_to_remove.append(bullet)
                
                # Creates a blast that hurts all enemies in given radius
                collision_circle = pygame.sprite.Sprite()
                collision_circle.rect = pygame.rect.Rect(enemy_hitted.x, enemy_hitted.y, 0, 0)
                collision_circle.radius = self.blast_radius
                enemies_collision = pygame.sprite.spritecollide(collision_circle, enemies, False, pygame.sprite.collide_circle)
                
                for enemy in enemies_collision:
                    enemy.lose_hp(self.blast_damage)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)