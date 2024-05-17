import pygame
from abc import ABC, abstractmethod

class Effect(ABC):
    
    # effect type should be an EffectType enum, damage, duration in seconds
    def __init__(self, effect_type, value, duration):
        
        self.effect_type = effect_type
        self.value = value
        self.duration = duration
        
        self.unpause_time = pygame.time.get_ticks()
        self.time_before_pause = 0
        
    def reset(self):
        self.unpause_time = pygame.time.get_ticks()
        
    def get_effect_type(self):
        return self.effect_type
    
    def get_color(self):
        return self.color

    def pause_effect(self):
        current_time = pygame.time.get_ticks()
        self.time_before_pause += current_time - self.unpause_time

    @abstractmethod
    def is_active(self):
        pass

    @abstractmethod
    def get_values(self):
        pass
    