import pygame
import sys
from game import Game

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tower defense")

    width, height = 1600, 900
    screen = pygame.display.set_mode((width, height), pygame.locals.RESIZABLE | pygame.locals.DOUBLEBUF, 16)

    cursor_image = pygame.image.load("assets/cursor.png").convert_alpha()
    cursor_surface = pygame.Surface(cursor_image.get_size(), pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))

    pygame.mouse.set_cursor((0, 0), cursor_surface)

    icon_image = pygame.image.load("assets/towers/archer_tower.png").convert_alpha()
    pygame.display.set_icon(icon_image)

    pygame.mixer.init()
    pygame.mixer.music.load("assets/music.mp3")  
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.015)

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()