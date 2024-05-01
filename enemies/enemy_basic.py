from enemies.enemy import Enemy

class EnemyBasic(Enemy):
    
    def __init__(self):
        
        Enemy.__init__(self, "assets/enemies/enemy.png")
        
        