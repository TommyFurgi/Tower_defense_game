import sys
 
import pygame
from pygame.locals import *
from map import Map 
from menu import Menu
from enemy import Enemy
from tower import Tower
from archer_tower import ArcherTower


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
hearts = 3

enemies = [Enemy()]

towers = pygame.sprite.Group() # defines a towers sprite group in pygame

edit_tower = pygame.sprite.GroupSingle() # this group holds single sprite

    


# makes selected tower follow player's mouse
def tower_drag(): # used to move tower around when selected from the menu
    
    edit_tower.draw(screen) # draws tower on a screen
    edit_tower.sprite.move() 

# selects a tower
def tower_pick_up(image):
                        
    edit_tower.add(ArcherTower(image))
    
# cancels placing a tower
def tower_cancel():
                    
    edit_tower.empty()

# places a tower if possible
def tower_place():
    
    if edit_tower.sprite.place():
                        
        towers.add(edit_tower.sprite)# add an instance of tower to group
        
        # TODO: Should substract certain amount of money from player's balance
                        
    edit_tower.empty() # removes sprite from the group

def move_all_enemies():
    to_delete  = []
    for monster in enemies:
        monster.draw(screen)
        if not monster.move():
            to_delete.append(monster)

    for monster_to_delete in to_delete:
        enemies.remove(monster_to_delete)
    
    if len(to_delete) - hearts < 0:
        ...
        # TODO end game

def update_screeen():
    menu.draw_all_menu(points, money, hearts)
    map.draw_background()

    move_all_enemies()


while True:

    update_screeen()
    
    if edit_tower.sprite: # tower was picked up
        tower_drag()
        
    towers.draw(screen) # automatically draws all towers, without user specified draw function
    towers.update() # calls each tower's update function
    
    
    move_all_enemies()

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == MOUSEBUTTONDOWN:
                
            if event.button == 1: # left mouse button
                    
                clicked_position = pygame.mouse.get_pos()
                    
                if menu.rect.collidepoint(clicked_position):
                        
                    image = menu.handle_click(clicked_position) # TODO: should return sth that could help to identify which tower was clicked
                        
                    if image != None and not edit_tower.sprite: # player is not holding a tower
                        tower_pick_up(image)
                    
            elif event.button == 3: # right mouse button
                
                if edit_tower.sprite: # tower is being held
                    tower_cancel()
                        
        elif event.type == MOUSEBUTTONUP:
                
            if event.button == 1: # left mouse button
                    
                if edit_tower.sprite: # tower is being held
                    tower_place()
                    
                    
            

    pygame.display.flip()
    fpsClock.tick(fps)