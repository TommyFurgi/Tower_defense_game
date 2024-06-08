import pygame
import sys
from game import Game
from source_manager import SourceManager


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tower defense")
    
    width, height = 1600, 900
    screen = pygame.display.set_mode((width, height), pygame.locals.RESIZABLE | pygame.locals.DOUBLEBUF, 16)

    SourceManager.load_all("./assets/images", "./assets/sounds", "./assets/environment", "paths.json")

    cursor_image = SourceManager.get_image("cursor").convert_alpha()
    cursor_surface = pygame.Surface(cursor_image.get_size(), pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))
    pygame.mouse.set_cursor((0, 0), cursor_surface)

    icon_image = SourceManager.get_image("archer_tower").convert_alpha()
    pygame.display.set_icon(icon_image)

    background_music = SourceManager.get_sound("background_music")
    background_music.play(loops = -1)
    SourceManager.set_sounds_volume(0.05)

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()