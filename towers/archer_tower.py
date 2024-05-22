import pygame
from towers.tower import Tower
from towers.bullet import Bullet
from effects.poison_effect import PoisonEffect
from source_manager import SourceManager
from towers.target import Target


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
        
        self.cooldown_timer = self.cooldown

        self.bullets = pygame.sprite.Group()
        self.update_tower_feature_rect()

        self.set_tower_target(Target.LEAST_HEALTH)
    

    def find_targets(self, enemies, delta_time):
        
        if self.cooldown_timer <= 0:
            
            enemy = self.get_tower_target(enemies)
            
            if enemy:
                
                self.cooldown_timer = self.cooldown
                enemy_x, enemy_y = enemy.get_position()
                self.bullets.add(Bullet(15, self.x, self.y-70, enemy_x, enemy_y - 60, enemy))
            
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
                if(enemy_hitted.add_effect(PoisonEffect(10, 3))): # Returns true if the effect was added, false if enemy is resistant to the effect
                    self.damage_dealt += 3 * 10
                actual_damage = enemy_hitted.lose_hp(self.damage)
                self.damage_dealt += actual_damage
                
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)



        
    
        
        
        