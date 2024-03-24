import sys
 
import pygame
from pygame.locals import *
from map import Map 
from menu import Menu
from enemy import Enemy
from tower import Tower


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1600, 900
#width, height = 1920, 1080

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tower defense")

map = Map(screen)
menu = Menu(screen)

money = 10000
points = 100

enemies = [Enemy(screen)]

towers = pygame.sprite.Group() # defines a towers sprite group in pygame

edit_tower = pygame.sprite.GroupSingle() # this group holds single sprite

def draw_window():
    menu.draw_all_menu(points, money, hearts=3)
    map.draw_background()

def edit_mode(): # used to move tower around when selected from the menu
        
    edit_tower.draw(screen) # draws tower on a screen
    edit_tower.sprite.follow_mouse() 

while True:

    draw_window()
    
    if edit_tower.sprite: # moving and drawing selected tower
        edit_mode() 
        
    towers.draw(screen) # automatically draws all towers, without user specified draw function
    
    enemies[0].draw(screen)
    enemies[0].move()
  
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == MOUSEBUTTONDOWN:
                
            if event.button == 1:  
                    
                clicked_position = pygame.mouse.get_pos()
                    
                if menu.rect.collidepoint(clicked_position):
                        
                    tower_image = menu.handle_click(clicked_position)
                        
                    edit_tower.add(Tower(tower_image))
                        
        elif event.type == MOUSEBUTTONUP:
            
              if edit_tower.sprite: #checks if edit_tower contains sprite
                
                if event.button == 1: # place a tower
                    
                    if edit_tower.sprite.place():
                        
                        towers.add(edit_tower.sprite)# add an instance of tower to group
                        
                    edit_tower.empty() # removes sprite from the group
            

    pygame.display.flip()
    fpsClock.tick(fps)