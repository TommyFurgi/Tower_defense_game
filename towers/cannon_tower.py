import pygame
from towers.tower import Tower
from towers.bullet import Bullet
from source_manager import SourceManager
from towers.target import Target


class CannonTower(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y)

        self.image = SourceManager.get_image("cannon_tower").convert_alpha()

        self.image = pygame.transform.scale(self.image, (150, 150))
        
        self.rect = pygame.Rect(x, y, 50, 50) 
        self.rect.center = (x, y) 
        
        self.damage = 150
        self.radius = 130
        self.cooldown = 1700
        self.price = 500
        
        self.cooldown_timer = self.cooldown
        
        self.blast_radius = 70
        self.blast_damage = 40
        
        self.bullets = pygame.sprite.Group()
        self.update_tower_feature_rect()

        self.set_tower_target(Target.FIRST)

        self.target_modes = [Target.FIRST, Target.LAST, Target.LEAST_HEALTH, Target.MOST_HEALTH]
        self.shot_sound = SourceManager.get_sound("cannon_shot")


        
    def find_targets(self, enemies, delta_time):

        if self.cooldown_timer <= 0:
            
            enemy = self.get_tower_target(enemies)
            
            if enemy:
                self.shot_sound.play()
                self.cooldown_timer = self.cooldown
                enemy_x, enemy_y = enemy.get_position()
                self.bullets.add(Bullet(25, self.x, self.y-70, enemy_x, enemy_y - 60, enemy))
                
        else:
            self.cooldown_timer -= delta_time

    def update(self, game_pasue, enemies, screen, delta_time):
        if not game_pasue:
            self.find_targets(enemies, delta_time)

        self.bullets.update(game_pasue, screen)

        bullets_to_remove = []
        
        for bullet in self.bullets:
            enemy_hitted = bullet.hit()
            if enemy_hitted:
                actual_damage = enemy_hitted.lose_hp(self.damage) 
                self.damage_dealt += actual_damage
                bullets_to_remove.append(bullet)
                
                # Creates a blast that hurts all enemies in given radius
                collision_circle = pygame.sprite.Sprite()
                collision_circle.rect = pygame.rect.Rect(enemy_hitted.x, enemy_hitted.y, 0, 0)
                collision_circle.radius = self.blast_radius
                enemies_collision = pygame.sprite.spritecollide(collision_circle, enemies, False, pygame.sprite.collide_circle)
                
                for enemy in enemies_collision:
                    actual_damage = enemy.lose_hp(self.blast_damage)
                    self.damage_dealt += actual_damage

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)