import sys
import pygame
from pygame.locals import *
from map import Map 
from menu import Menu
from enemies.enemy import Enemy
from towers.tower import Tower
from towers.archer_tower import ArcherTower
from editor import Editor
import math

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1600, 900
#width, height = 1920, 1080

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tower defense")

map = Map(screen)
menu = Menu(screen)

# path =  [(520, 790), (530, 750), (550, 725), (580, 680), (600, 660), (640, 650), (660, 645), (680, 620), (695, 585), (700, 565), (695, 540), (686, 525), (683, 495), 
#                  (678, 460), (660, 445), (635, 440), (610, 430), (580, 420), (570, 410),  (560, 400), (550, 390), (525, 380), (505, 370), (480, 360), (460, 335), (455, 320), 
#                  (450, 300), (452, 285), (455, 265), (470, 250), (485, 230), (500, 210), (515, 200), (530, 180), (550, 180), (570, 180), (590, 180), (610, 180), (630, 180), 
#                  (650, 180), (670, 180), (690, 180), (710, 180), (730, 180), (750, 180), (770, 180), (790, 180), (810, 180), (830, 180), (850, 180), (870, 180), (890, 180), 
#                  (910, 180), (930, 180), (950, 180), (970, 180), (990, 180), (1010, 180), (1030, 180), (1050, 180), (1070, 180), (1090, 180), (1110, 180), (1130, 180), 
#                  (1150, 180), (1170, 180), (1190, 180), (1210, 180), (1230, 180), (1250, 180), (1270, 180), (1290, 180), (1310, 180), (1330, 180), (1350, 180)]

path = [
    (539, 892), (541, 868), (543, 837), (547, 806), (555, 771),
    (570, 750), (587, 732), (607, 717), (632, 706), (659, 699),
    (677, 693), (692, 667), (699, 638), (702, 597), (695, 569),
    (688, 544), (676, 530), (660, 515), (646, 503), (627, 496),
    (606, 493), (574, 479), (550, 470), (523, 457), (501, 429),
    (481, 409), (472, 383), (470, 354), (462, 319), (467, 289),
    (475, 263), (487, 240), (503, 229), (525, 214), (547, 207),
    (573, 205), (595, 204), (615, 201), (637, 200), (680, 199),
    (717, 198), (752, 198), (787, 197), (816, 199), (853, 199),
    (895, 195), (935, 193), (979, 193), (1019, 194), (1055, 194),
    (1098, 191), (1147, 192), (1195, 192), (1246, 190), (1289, 190),
    (1329, 191), (1353, 191)
]


money = 10000
points = 100
hearts = 3

game_pause = True

enemies = []
towers = []
spawn_interval = 500 
last_spawn_time = 0
enemies_to_generate = 30
drag_object = None
selected_tower = None

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


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     

def drag_object_conflict(drag_object):

    # for tower in towers:
        # if pygame.Rect.colliderect(tower, drag_object):
        
    #if drag_object.collide_rect():
    # if calculate_distance(clicked_position[0], clicked_position[1], tower.x, tower.y) < 100:
    #    return True
    
    return pygame.sprite.spritecollide(drag_object, towers, False) # [] is eveluated as False    
    
    #for path_point in path:
    #    dist = calculate_distance(clicked_position[0], clicked_position[1], path_point[0], path_point[1])
    #    if dist < 70:
    #        return True

    #return clicked_position[0] > 1320

def update_screen():
    
    menu.draw_all_menu(points, money, hearts)
    map.draw_background()

    for tower in towers:
        tower.draw(screen)

    if drag_object:
        
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        drag_object.rect.center = (mouse_x, mouse_y - 60)

        color = (0, 0, 255, 100)
        if drag_object_conflict(drag_object):
            color = (255, 0, 0, 100)
        
        surface = pygame.Surface((160, 160), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, color, (80, 80), 80, 0)
        screen.blit(surface, (mouse_x - 80, mouse_y - 80))

        screen.blit(drag_object.image, drag_object.rect)
    
    
def update_game():
    global last_spawn_time, enemies_to_generate

    move_all_enemies()

    current_time = pygame.time.get_ticks()
    if enemies_to_generate > 0 and current_time - last_spawn_time >= spawn_interval:
        enemies.append(Enemy(path))
        enemies_to_generate -= 1
        last_spawn_time = current_time

# Editor related
editor = Editor(screen, "environment/path")
edit_mode = False

while True:
    update_screen()

    if edit_mode:
        editor.edit()
        pygame.display.flip() # Required by editor
        continue

    if not game_pause:
        update_game()
    
    
    move_all_enemies()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_position = pygame.mouse.get_pos()
                print(clicked_position)

                if not drag_object:
                    if selected_tower:
                        selected_tower.selected = False
                        selected_tower = None

                    if menu.rect.collidepoint(clicked_position):
                        drag_object, drag_object_name = menu.handle_click(clicked_position)
                        
                        # drag_object = pygame.image
                        temp_sprite = pygame.sprite.Sprite()
                        temp_sprite.image = drag_object
                        temp_sprite.rect = drag_object.get_rect()
                        drag_object = temp_sprite
                        

                    for tower in towers:
                        if tower.click(clicked_position[0], clicked_position[1]):
                            selected_tower = tower
                            break

                elif drag_object and not drag_object_conflict(drag_object):
                    match drag_object_name:
                        case "archer":
                            tower = ArcherTower(clicked_position[0], clicked_position[1]-60, screen)

                    towers.append(tower)
                    drag_object = None


            elif event.button == 3:
                if selected_tower:
                        selected_tower.selected = False
                        selected_tower = None

                drag_object = None
                drag_object_name = None

    pygame.display.flip()
    fpsClock.tick(fps)

