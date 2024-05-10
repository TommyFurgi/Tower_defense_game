
class EnemyWave():
    
    def __init__(self, enemies):
        self.enemies = enemies
        self.current = 0
        self.current_enemy = 0
        
    def get_next_enemy(self):
        
        if self.current >= len(self.enemies):
            raise Exception("Wave has ended!")
        
        if self.current_enemy < self.enemies[self.current][1]:
            self.current_enemy += 1
            return self.enemies[self.current][0]
        else:
            self.current_enemy = 0
            self.current += 1
        
    def isFinished(self):
        return self.current >= len(self.enemies)