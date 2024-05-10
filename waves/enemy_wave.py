
class EnemyWave():
    
    def __init__(self, enemies):
        self.enemies = enemies
        self.current_enemy_type = 0
        self.current_enemy = 0
        
    def get_next_enemy(self):
        
        if not self.has_next_enemy():
            raise Exception("Wave has ended!")
        
        if self.current_enemy < self.enemies[self.current_enemy_type][1]:
            self.current_enemy += 1
            return self.enemies[self.current_enemy_type][0]
        else:
            self.current_enemy = 0
            self.current_enemy_type += 1
        
    def has_next_enemy(self):
        return self.current_enemy_type < len(self.enemies)