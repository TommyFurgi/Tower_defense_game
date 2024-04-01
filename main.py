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

game_pause = False

enemies = []
spawn_interval = 500 
last_spawn_time = 0
enemies_to_generate = 30

towers = pygame.sprite.Group()
edit_tower = pygame.sprite.GroupSingle()

def tower_drag():
    edit_tower.draw(screen)
    edit_tower.sprite.move() 

def tower_pick_up(image):
    edit_tower.add(ArcherTower(image))
    
def tower_cancel():
    edit_tower.empty()

def tower_place():
    if edit_tower.sprite.place():
        towers.add(edit_tower.sprite)
    edit_tower.empty()

def move_all_enemies():
    global money, hearts
    to_delete = []
    for monster in enemies:
        monster.draw(screen)
        if not monster.move():
            to_delete.append(monster)

    for monster_to_delete in to_delete:
        enemies.remove(monster_to_delete)
        money -= 100
        hearts -= 1
    
    if len(to_delete) - hearts < 0:
        pass  # TODO: end game

def update_screen():
    
    menu.draw_all_menu(points, money, hearts)
    map.draw_background()
    
def update_game():
    global last_spawn_time, enemies_to_generate

    move_all_enemies()

    current_time = pygame.time.get_ticks()
    if enemies_to_generate > 0 and current_time - last_spawn_time >= spawn_interval:
        enemies.append(Enemy())
        enemies_to_generate -= 1
        last_spawn_time = current_time

while True:
    update_screen()

    if not game_pause:
        update_game()
    
    if edit_tower.sprite:
        tower_drag()
        
    towers.draw(screen)
    towers.update()
    
    move_all_enemies()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_position = pygame.mouse.get_pos()
                if menu.rect.collidepoint(clicked_position):
                    image = menu.handle_click(clicked_position)
                    if image != None and not edit_tower.sprite:
                        tower_pick_up(image)
            elif event.button == 3:
                if edit_tower.sprite:
                    tower_cancel()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if edit_tower.sprite:
                    tower_place()

    pygame.display.flip()
    fpsClock.tick(fps)
