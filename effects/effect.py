import pygame
from effects.effect_type import EffectType

class Effect():
    
    # effect type should be an EffectType enum, damage, duration in seconds
    def __init__(self, effect_type, damage, duration):
        
        self.__effect_type = effect_type
        self.__damage = damage
        self.__duration = duration
        self.__start_time = pygame.time.get_ticks()
        self.__time_since_last_hit = self.__start_time
    
    def reset(self):
        self.__start_time = pygame.time.get_ticks()
    
    def update(self):
        
        current_time = pygame.time.get_ticks()
        
        if(current_time - self.__start_time <= self.__duration * 1000):
            damage_to_deal = self.calcualte_damage(current_time)
            self.__time_since_last_hit = current_time
            return self.__effect_type, damage_to_deal
        else:
            return EffectType.EFFECT_FINISHED, None
        
    def calcualte_damage(self, time):
        return ( self.__damage * (time - self.__time_since_last_hit) ) / (self.__duration * 1000)
        
    def get_effect_type(self):
        return self.__effect_type
    
    def get_damage_per_second(self):
        return self.__damage
    
    