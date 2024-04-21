import pygame
import sys
from game import Game

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tower defense")

    cursor_image = pygame.image.load("assets/cursor.png") 
    cursor_surface = pygame.Surface(cursor_image.get_size(), pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))

    pygame.mouse.set_cursor((0, 0), cursor_surface)

    icon_image = pygame.image.load("assets/towers/archer_tower.png")  
    pygame.display.set_icon(icon_image)

    width, height = 1600, 900
    screen = pygame.display.set_mode((width, height))

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()