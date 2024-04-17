import pygame


"""

Debug class in used to visualize all rects on the screen
in order to diagnose errors with collision. Shouldn't be
used while edit mode is active.

"""

class Debug():
    
    def __init__(self, screen):
        self.screen = screen
    
    
    # Draws all rectangles responsible for path collisions
    def draw_paths_rect(self, path):

        for pth in path:

            rect_surface = pygame.Surface((pth.rect.w, pth.rect.h), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (pth.rect.x, pth.rect.y))
        
    # Draws drag_object rect in real time
    def draw_drag_object_rect(self, drag_object):
        
        rect_surface = pygame.Surface((drag_object.rect.w, drag_object.rect.h), pygame.SRCALPHA)
        rect_surface.fill((255, 0, 0, 128))
        self.screen.blit(rect_surface, (drag_object.rect.x, drag_object.rect.y))
    
    # Draws all rectangles responsible for other collisions
    def draw_others_rect(self, others):

        for othr in others:

            rect_surface = pygame.Surface((othr.rect.w, othr.rect.h), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (othr.rect.x, othr.rect.y))
            
    def draw_enemy_rect(self, enemies):

        for enemy in enemies:

            rect_surface = pygame.Surface((enemy.rect.w, enemy.rect.h), pygame.SRCALPHA)
            rect_surface.fill((255, 0, 0, 128))
            self.screen.blit(rect_surface, (enemy.rect.x, enemy.rect.y))
            
        