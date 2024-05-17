from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class SlowDownEffect(Effect):
    
    def __init__(self, value, duration):
        
        Effect.__init__(self, EffectType.SLOWDOWN, value, duration)
        self.color = (104, 141, 242)
        
    def get_values(self):
        return self.value, self.color

    def is_active(self):

        if (pygame.time.get_ticks() - self.unpause_time <= self.duration * 1000 - self.time_before_pause):
            return True
        return False
        