import json
from collections import OrderedDict
from waves.enemy_wave import EnemyWave

WAVE_FILENAME = "waves/waves.json"


class WaveManager():
    """
    WaveManager loads waves from JSON and creates EnemyWave object
    for each wave from "waves.json" file.
    """
    def __init__(self):
        self.waves_loaded = self.load_waves()
        
        self.waves = [wave for wave in self.waves_loaded]
        self.current_wave = 0
    
    
    def load_waves(self):
        """Loads waves data from json."""
        waves_read = []

        with open(WAVE_FILENAME, 'r') as f:
            waves_read = json.load(f, object_pairs_hook=OrderedDict)
        
        return waves_read
    
    
    def get_next_wave(self):
        """Returns wave object containing information about enemies."""
        if not self.has_next_wave():
            raise Exception("No more waves!")

        enemies = []
        
        for enemy in self.waves_loaded[self.waves[self.current_wave]]:
            enemies.append((enemy, self.waves_loaded[self.waves[self.current_wave]][enemy]))

        self.current_wave += 1

        return EnemyWave(enemies)


    def has_next_wave(self):
        """Checks if there is one more wave."""
        return self.current_wave < len(self.waves)
