import sys
 
import pygame
from pygame.locals import *
from map import Map 
from menu import Menu


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1600, 900
#width, height = 1920, 1080

screen = pygame.display.set_mode((width, height))
map = Map(screen)
menu = Menu(screen)

money = 10000
points = 100
def draw_window():
    menu.draw_all_menu(points, money, hearts=3)


while True:

    draw_window()

  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  
                clicked_position = pygame.mouse.get_pos()
                
                if menu.rect.collidepoint(clicked_position):
                    menu.handle_click(clicked_position)
 
 
    pygame.display.flip()
    fpsClock.tick(fps)