from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class SlowDownEffect(Effect):
    
    def __init__(self, property, duration):
        
        Effect.__init__(self, EffectType.SLOWDOWN, property, duration)
        self.color = (104, 141, 242)

    def update(self):
        
        current_time = pygame.time.get_ticks()
        
        if (current_time - self.unpause_time <= self.duration * 1000 - self.time_before_pause):
            return self.effect_type, self.property, self.color
        else:
            return EffectType.EFFECT_FINISHED, None, self.color
        
        