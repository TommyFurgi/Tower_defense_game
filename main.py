import sys
 
import pygame
from pygame.locals import *
from background import Back_ground 


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1650, 900
screen = pygame.display.set_mode((width, height))

back_ground = Back_ground('map.jpg', [0,0])
# menu = Menu(,[])
def draw_window():

    screen.fill([255, 255, 255])
    screen.blit(back_ground.image, back_ground.rect)


# Game loop.
while True:

    draw_window()
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
  
  # Update.
  
  # Draw.
  
    pygame.display.flip()
    fpsClock.tick(fps)