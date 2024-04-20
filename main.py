import pygame
from game import Game

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tower defense")

    game = Game()
    game.run()