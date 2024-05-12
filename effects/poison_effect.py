from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class PoisonEffect(Effect):
    
    def __init__(self, property, duration):
        
        Effect.__init__(self, EffectType.POISION, property, duration)
        
        self.current_time = pygame.time.get_ticks() + 1500 # Zeby efekt zaczął działać od razu, a nie dopiero po 1,5 sekundy
        
        self.demage_counter = duration
        self.demage = property
        self.color = (36, 77, 28) 
        #self.color = (100, 255, 100)
    
    def update(self):

        if self.demage_counter == 0:
            return EffectType.EFFECT_FINISHED, None, self.color
        
        elif (self.current_time - self.unpause_time >= 1500 - self.time_before_pause):
            self.unpause_time = self.current_time
            self.demage_counter -= 1
            return self.effect_type, self.demage, self.color
        
        self.current_time = pygame.time.get_ticks()
        
        return None, None, None # Waiting
