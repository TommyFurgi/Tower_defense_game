import sys
 
import pygame
from pygame.locals import *
from background import Background 


pygame.init()
BackGround = Background('map.jpg', [0,0])

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1800, 1000
screen = pygame.display.set_mode((width, height))
 
# Game loop.
while True:
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
  
  # Update.
  
  # Draw.
  
    pygame.display.flip()
    fpsClock.tick(fps)