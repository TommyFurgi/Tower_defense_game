import sys
 
import pygame
from pygame.locals import *
from background import Back_ground 
from menu import Menu


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1650, 900
#width, height = 1920, 1080

screen = pygame.display.set_mode((width, height))

back_ground = Back_ground('img/map.jpg', screen)
menu = Menu(screen)
screen.blit(back_ground.image, back_ground.rect)



def draw_window():
    menu.draw_points(100)
    menu.draw_money(10000)
    menu.draw_hearts(3)


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