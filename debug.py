import pygame

class Debug():
    """
    A class that provides debugging functionality for a game screen.
    
    Attributes:
        screen (pygame.Surface): The game screen to draw on.
    """
    
    def __init__(self, screen):
        self.screen = screen
    
    def draw_paths_rect(self, path):
        """
        Draws rectangles for the given path on the game screen.
        
        Args:
            path (list): A list of path objects.
        """
        for pth in path:
            rect_surface = pygame.Surface((pth.rect.w, pth.rect.h), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (pth.rect.x, pth.rect.y))
        
    def draw_drag_object_rect(self, drag_object):
        """
        Draws a rectangle for the drag object on the game screen in real time.
        
        Args:
            drag_object: The drag object to draw.
        """
        rect_surface = pygame.Surface((drag_object.rect.w, drag_object.rect.h), pygame.SRCALPHA)
        rect_surface.fill((255, 0, 0, 128))
        self.screen.blit(rect_surface, (drag_object.rect.x, drag_object.rect.y))
    
    def draw_others_rect(self, others):
        """
        Draws rectangles for other collisions on the game screen.
        
        Args:
            others (list): A list of other collision objects.
        """
        for othr in others:
            rect_surface = pygame.Surface((othr.rect.w, othr.rect.h), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (othr.rect.x, othr.rect.y))
            
    def draw_enemy_rect(self, enemies):
        """
        Draws rectangles for enemies on the game screen.
        
        Args:
            enemies (list): A list of enemy objects.
        """
        for enemy in enemies:
            rect_surface = pygame.Surface((enemy.rect.w, enemy.rect.h), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (enemy.rect.x, enemy.rect.y))
            
        