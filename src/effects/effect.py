import pygame
from abc import ABC, abstractmethod

class Effect(ABC):
    """
    Abstract class which defines effect behaviour. Requires each
    effect to implement is_active and get_values.
    """
    
    # effect type should be an EffectType enum, damage, duration in seconds
    def __init__(self, effect_type, value, duration):
        
        self.effect_type = effect_type
        self.value = value
        self.duration = duration
        
        self.unpause_time = pygame.time.get_ticks()
        self.time_before_pause = 0
        
        
    def reset(self):
        """Allows an effect to be paused."""
        self.unpause_time = pygame.time.get_ticks()
        
        
    def get_effect_type(self):
        """Returns effect's type."""
        return self.effect_type
    
    
    def get_color(self):
        """Returns effect's color."""
        return self.color


    def pause_effect(self):
        """Allows an effect to be paused."""
        current_time = pygame.time.get_ticks()
        self.time_before_pause += current_time - self.unpause_time


    @abstractmethod
    def is_active(self):
        """Should check if effect is aactive and update its alive time."""
        pass


    @abstractmethod
    def get_values(self):
        """Should return effects value."""
        pass
    