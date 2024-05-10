import json
from collections import OrderedDict
from enemy_wave import EnemyWave

WAVE_FILENAME = "waves.txt"

class WaveManager():

    def __init__(self):
        
        self.waves_loaded = self.load_waves()
        
        self.waves = [wave for wave in self.waves_loaded]
        self.current_wave = 0
    
    # loads waves data from json
    def load_waves(self):
        
        waves_read = []

        with open(WAVE_FILENAME, 'r') as f:
            waves_read = json.load(f, object_pairs_hook=OrderedDict)
            
        return waves_read
    
    # returns wave object containing information about enemies
    def get_next_wave(self):

        if not self.has_next_wave():
            raise Exception("No more waves!")

        enemies = []
        
        for enemy in self.waves_loaded[self.waves[self.current_wave]]:
            enemies.append((enemy, self.waves_loaded[self.waves[self.current_wave]][enemy]))

        self.current_wave += 1

        return EnemyWave(enemies)
    
    def has_next_wave(self):
        return self.current_wave < len(self.waves)
    
# waves = dict()
#wave_enemies = dict()

#wave_enemies["basic"] = 5
#wave_enemies["boss"] = 1

#waves["wave_1"] = wave_enemies
#waves["wave_2"] = wave_enemies