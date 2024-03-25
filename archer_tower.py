import pygame
from tower import Tower
from menu import Menu

class ArcherTower(Tower):
    
     # player grabbed a tower from the menu
    def __init__(self, image):
        Tower.__init__(self, image)

    def update(self):
        # print("pow pow pow")
        
        #self.find_targets()
        
        pass
    
    def find_targets(self):
        
        # TODO: create circular surface and check if it overlapps enemies
        
        pass


        
    
        
        
        