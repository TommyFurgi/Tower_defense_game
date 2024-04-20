import sys
import pygame
import math
from pygame.locals import *
from map import Map 
from menu import Menu
from enemies.enemy import Enemy
from towers.tower import Tower
from towers.archer_tower import ArcherTower
from editor import Editor
from debug import Debug

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1600, 900
#width, height = 1920, 1080

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tower defense")

game_map = Map(screen)
menu = Menu(screen)

money = 10000
points = 0
hearts = 3

game_pause = False

#enemies = pygame.sprite.OrderedUpdates() # Cos jak grupa tylko rysuje sprite'y w kolejnosci dodania (Wtedy trzeba chyba uzyc enemies.draw())
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()
paths = pygame.sprite.Group()
others = pygame.sprite.Group()

spawn_interval = 700 
last_spawn_time = 0
enemies_to_generate = 15
drag_object = None
selected_tower = None

# # Editor related
# editor = [Editor(screen, "environment/path"),
#           Editor(screen, "environment/others")]
# edit_mode = False

# # Debug related
# debug = Debug(screen)
# debug_mode = False

def load_rectangles_from_file(filename):
    try:
        with open(filename, "r") as file:
            rectangles = []
            for line in file:
                rect_x, rect_y, rect_width, rect_height = map(int, line.strip().split())
                rectangles.append((rect_x, rect_y, rect_width, rect_height))
    except FileNotFoundError:
        print(f"File '{filename}' not found. No rectangles loaded.")
    
    return rectangles


def check_all_enemies():
    global money, hearts, game_pause, points
    enemies_on_end =[]
    killed_enemies = []

    for monster in enemies:
        is_killed, reward = monster.is_killed()
        if is_killed:
            killed_enemies.append((monster, reward))
            continue

        if monster.to_delete():
            enemies_on_end.append(monster)


    for monster_to_delete, reward in killed_enemies:
        enemies.remove(monster_to_delete)
        money += reward
        points += 200

    for monster_to_delete in enemies_on_end:
        enemies.remove(monster_to_delete)
        points -= 500
        money -= 100
        hearts -= 1

        if hearts <= 0:
            game_pause = True
            # TODO: end game


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     

def drag_object_conflict(drag_object):

    return (pygame.sprite.spritecollide(drag_object, towers, False) or 
            pygame.sprite.spritecollide(drag_object, paths, False) or
            pygame.sprite.spritecollide(drag_object, others, False))  

def update_screen():
    
    menu.draw_all_menu(points, money, hearts)
    game_map.draw_background()

    if drag_object:
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        drag_object.rect.center = (mouse_x, mouse_y)

        color = (0, 0, 255, 100)
        if drag_object_conflict(drag_object):
            color = (255, 0, 0, 100)
        
        surface = pygame.Surface((160, 160), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, color, (80, 80), 80, 0)
        screen.blit(surface, (mouse_x - 80, mouse_y - 80))

        screen.blit(drag_object.image, (mouse_x - 80, mouse_y - 120))
    
def update_game(game_pause):
    global last_spawn_time, enemies_to_generate

    towers.update(game_pause, enemies, screen)
    enemies.update(game_pause)
    

    if not game_pause:
        check_all_enemies()

        current_time = pygame.time.get_ticks()
        if enemies_to_generate > 0 and current_time - last_spawn_time >= spawn_interval:
            enemies.add(Enemy(screen))

            enemies_to_generate -= 1
            last_spawn_time = current_time

# Loads rectangles from file and adds them to group
def load_rects(filename, group):
    
    rectangles = load_rectangles_from_file(filename)
    
    for rectangle in rectangles:
        
        rect_sprite = pygame.sprite.Sprite()
        rect_sprite.rect = pygame.Rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3])

        group.add(rect_sprite)

load_rects("environment/path", paths)
load_rects("environment/others", others)
        
while True:
    update_screen()

    # if debug_mode:
    #     debug.draw_paths_rect(paths)
    #     debug.draw_others_rect(others)
    #     debug.draw_enemy_rect(enemies)
    #     if drag_object:
    #         debug.draw_drag_object_rect(drag_object)

    # if edit_mode:
    #     editor[1].edit()
    #     pygame.display.flip() # Required by editor
    #     continue

    update_game(game_pause)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_position = pygame.mouse.get_pos()
                # print(clicked_position)

                if not drag_object:
                    if selected_tower:
                        selected_tower.selected = False
                        selected_tower = None

                    if menu.rect.collidepoint(clicked_position):
                        drag_object, drag_object_name = menu.handle_click(clicked_position)
                        
                        if not drag_object:
                            if drag_object_name == "play":
                                game_pause = False
                            elif drag_object_name == "stop":
                                game_pause = True

                            continue

                        # drag_object = pygame.image
                        temp_sprite = pygame.sprite.Sprite()
                        temp_sprite.image = drag_object
                        temp_sprite.rect = pygame.rect.Rect(clicked_position[0], clicked_position[1], 50, 50)
                        drag_object = temp_sprite
                        

                    for tower in towers:
                        if tower.click(clicked_position[0], clicked_position[1]):
                            selected_tower = tower
                            break

                elif drag_object and not drag_object_conflict(drag_object):
                    match drag_object_name:
                        case "archer":
                            tower = ArcherTower(clicked_position[0]-3, clicked_position[1]-42, screen)

                    towers.add(tower)
                    drag_object = None


            elif event.button == 3:
                if selected_tower:
                        selected_tower.selected = False
                        selected_tower = None

                drag_object = None
                drag_object_name = None

    pygame.display.flip()
    fpsClock.tick(fps)

