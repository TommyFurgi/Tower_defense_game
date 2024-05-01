import pygame
from abc import ABC, abstractmethod

class Effect(ABC):
    
    # effect type should be an EffectType enum, damage, duration in seconds
    def __init__(self, effect_type, property, duration):
        
        self.effect_type = effect_type
        self.property = property
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
    
    @abstractmethod
    def update(self):
        pass
        
    def reset(self):
        self.start_time = pygame.time.get_ticks()
        
    def get_effect_type(self):
        return self.effect_type
    
    def get_property(self):
        return self.property
    
    