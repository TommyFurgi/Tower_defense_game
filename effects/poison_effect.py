from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class PoisonEffect(Effect):
    
    def __init__(self, property, duration):
        
        Effect.__init__(self, EffectType.POISION, property, duration)
        
        self.demage_counter = duration
        self.demage = property
        self.color = (36, 77, 28)
    
    
    def update(self):

        current_time = pygame.time.get_ticks()

        if self.demage_counter == 0:
            return EffectType.EFFECT_FINISHED, None, None
        
        elif (current_time - self.unpause_time >= 1500 - self.time_before_pause):
            self.unpause_time = current_time
            self.demage_counter -= 1
            return self.effect_type, self.demage, self.color
        
        return None, None, None
