from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class PoisonEffect(Effect):
    """A variant of an Effect, makes player lose health over time."""
    def __init__(self, value, duration):
        
        Effect.__init__(self, EffectType.POISON, value, duration)
        
        self.current_time = pygame.time.get_ticks() + 1500 # Zeby efekt zaczął działać od razu, a nie dopiero po 1,5 sekundy
        
        self.demage_counter = duration
        self.demage = value
        self.color = (36, 77, 28) 
        #self.color = (100, 255, 100)


    def update(self):
        """Called every frame. Updates effects duration."""
        if (self.current_time - self.unpause_time >= 1500 - self.time_before_pause):
            self.unpause_time = self.current_time
            self.demage_counter -= 1
            return self.demage, self.color
        
        self.current_time = pygame.time.get_ticks()
        
        return None, None # Waiting
    
    
    def get_values(self):
        """Returns effects value and it's color."""
        return self.value, self.color


    def is_active(self):
        """Determines if effect is still active."""
        return self.demage_counter > 0
            