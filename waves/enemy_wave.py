import pygame
from enemies.enemy_basic import EnemyBasic
from enemies.enemy_magic import EnemyMagic
from enemies.enemy_boss import EnemyBoss

class EnemyWave():
    
    def __init__(self, enemies):
        
        self.basic_no = 0
        self.magic_no = 0
        self.boss_no = 0

        for enemy_name, enemy_number in enemies:
            match enemy_name:
                    case "basic":
                        self.basic_no = enemy_number
                    case "magic":
                        self.magic_no = enemy_number
                    case "boss":
                        self.boss_no = enemy_number

        self.basic_enemy_spawn_time = 0
        self.magic_enemy_spawn_time = 0
        self.boss_enemy_spawn_time = 0

        self.basic_time_before_pause = pygame.time.get_ticks()
        self.magic_time_before_pause = pygame.time.get_ticks()
        self.boss_time_before_pause = pygame.time.get_ticks()


        self.normal_spawn_interval = 700
        self.boss_spawn_interval = 1500 
            
        
    def get_next_enemy(self):
        current_time = pygame.time.get_ticks()

        if not self.has_next_enemy():
            raise Exception("Wave has ended!")

        if self.basic_no and current_time - self.basic_enemy_spawn_time >= self.normal_spawn_interval - self.basic_time_before_pause:
            self.basic_enemy_spawn_time = current_time
            self.basic_no -= 1
            self.basic_time_before_pause = 0
            return EnemyBasic()
        
        if self.magic_no and current_time - self.magic_enemy_spawn_time >= self.normal_spawn_interval - self.magic_time_before_pause:
            self.magic_enemy_spawn_time = current_time
            self.magic_no -= 1
            self.magic_time_before_pause = 0
            return EnemyMagic()
        
        if self.boss_no and current_time - self.boss_enemy_spawn_time >= self.boss_spawn_interval - self.boss_time_before_pause:
            self.boss_enemy_spawn_time = current_time
            self.boss_no -= 1
            self.boss_time_before_pause = 0
            return EnemyBoss()
        
        return None
        
    def has_next_enemy(self):
        return self.basic_no + self.magic_no + self.boss_no
    

    def reset_spawn_time(self):
        self.basic_enemy_spawn_time = pygame.time.get_ticks()
        self.magic_enemy_spawn_time = pygame.time.get_ticks()
        self.boss_enemy_spawn_time = pygame.time.get_ticks()

        

    def pause_spawn_time(self):
        current_time = pygame.time.get_ticks()
        self.basic_time_before_pause +=  current_time - self.basic_enemy_spawn_time
        self.magic_time_before_pause += current_time - self.magic_enemy_spawn_time
        self.boss_time_before_pause += current_time - self.boss_enemy_spawn_time