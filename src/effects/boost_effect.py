from effects.effect import Effect
from effects.effect_type import EffectType
import pygame

class BoostEffect(Effect):
    """A variant of an Effect, makes player go faster."""
    def __init__(self, value, duration):
        
        Effect.__init__(self, EffectType.BOOST, value, duration)
        self.color = (168, 184, 31)
    
    
    def get_values(self):
        """Returns effects value and it's color."""
        return self.value, self.color
        
        
    def is_active(self):
        """Determines if effect is still active."""
        return pygame.time.get_ticks() - self.unpause_time <= self.duration * 1000 - self.time_before_pause
        
        
