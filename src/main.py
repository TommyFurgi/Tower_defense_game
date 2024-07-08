import pygame
import sys
from game import Game
from resource_manager import ResourceManager

def main():
    """
    Initialize and run the Tower Defense game.

    Initializes Pygame, sets up the game window, loads assets, sets up cursor and icon,
    starts background music, creates a Game instance, and runs the game loop until the
    user quits.
    """
    pygame.init()
    pygame.display.set_caption("Tower defense")
    
    width, height = 1600, 900
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF, 16)

    # Load all game assets
    ResourceManager.load_all("./assets/images", "./assets/sounds", "./assets/environment", "paths.json")

    # Set custom cursor
    cursor_image = ResourceManager.get_image("cursor").convert_alpha()
    cursor_surface = pygame.Surface(cursor_image.get_size(), pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))
    pygame.mouse.set_cursor((0, 0), cursor_surface)

    # Set window icon
    icon_image = ResourceManager.get_image("archer_tower").convert_alpha()
    pygame.display.set_icon(icon_image)

    # Play background music
    background_music = ResourceManager.get_sound("background_music")
    background_music.play(loops=-1)
    ResourceManager.set_sounds_volume(0.05)

    # Initialize and run the game
    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
