from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class PoisonEffect(Effect):
    
    def __init__(self, property, duration):
        
        Effect.__init__(self, EffectType.POISION, property, duration)
        
        self.time_since_last_hit = 0
        self.demage_counter = duration
        self.demage = property
    
    # def calcualte_damage(self, time):
    #     return ( self.property * (time - self.time_since_last_hit) ) / (self.duration * 1000)
    
    def update(self):

        current_time = pygame.time.get_ticks()

        if self.demage_counter == 0:
            return EffectType.EFFECT_FINISHED, None
        
        elif (current_time - self.time_since_last_hit >= 1500):
            # damage_to_deal = self.calcualte_damage(current_time)
            self.time_since_last_hit = current_time
            self.demage_counter -= 1
            return self.effect_type, self.demage
        
        return None, None
