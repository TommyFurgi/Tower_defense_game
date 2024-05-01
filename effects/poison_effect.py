from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class PoisonEffect(Effect):
    
    def __init__(self, property, duration):
        
        Effect.__init__(self, EffectType.POISION, property, duration)
        
        self.time_since_last_hit = self.start_time
    
    def calcualte_damage(self, time):
        return ( self.property * (time - self.time_since_last_hit) ) / (self.duration * 1000)
    
    def update(self):
        
        current_time = pygame.time.get_ticks()
        
        if(current_time - self.start_time <= self.duration * 1000):
            damage_to_deal = self.calcualte_damage(current_time)
            self.time_since_last_hit = current_time
            return self.effect_type, damage_to_deal
        else:
            return EffectType.EFFECT_FINISHED, None