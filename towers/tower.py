from typing import Any
import pygame
from abc import ABC, abstractmethod
from towers.bullet import Bullet


class Tower(pygame.sprite.Sprite, ABC): 
    
    def __init__(self, x, y): 

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.level = 1
        self.selected = False

        self.tower_imgs = []
        self.damage = 100
        self.range = 150
        self.cooldown = 700
        self.time_from_last_shot = pygame.time.get_ticks()
        
        self.radius = self.range

        self.bullets = pygame.sprite.Group()
        
    def draw(self, screen):
        image = self.tower_imgs[self.level-1]

        if self.selected:
            self.draw_radius(screen)
            # TODO: draw menu for upgrade

    
        screen.blit(image, (self.x-image.get_width()//2, self.y-image.get_height()//2))


    def draw_radius(self, screen):
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 255, 100), (self.range, self.range), self.range, 0)

        screen.blit(surface, (self.x - self.range, self.y - self.range))



    def click(self, X, Y):
        img = self.tower_imgs[self.level - 1]
        if abs(X-self.x) < img.get_width()//2:
            if abs(Y-self.y) < img.get_height()//2:
                self.selected = True
                
                return True
        return False
    
    def find_targets(self, enemies):
        
        # True znaczy, że obiekty, które wejdą w kolizję z okręgiem dookoła wieży są usuwane
        # TODO: zmienić True na False i zamiast tego dodać zadawanie obrażeń
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        if enemies_collision and pygame.time.get_ticks() - self.time_from_last_shot > self.cooldown:
            self.time_from_last_shot = pygame.time.get_ticks()
            # enemies_collision[0].lose_hp(self.damage)
            enemy_x, enemy_y = enemies_collision[0].get_position()
            self.bullets.add(Bullet(self.x, self.y-70, enemy_x, enemy_y - 60, enemies_collision[0]))
            

    
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

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

        self.draw(screen)
        
    
    
        
        
        