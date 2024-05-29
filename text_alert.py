import pygame 

class TextAlert():
    def __init__(self, text, duration, color, x_scale_rate, y_scale_rate):
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.x = 800
        self.y = 450
        self.text = text
        self.duration = duration
        
        self.color = color
        self.font = pygame.font.Font(None, int(50 * self.x_scale_rate))
        
        self.outline_color = (0, 0, 0)
        
        self.creation_time = pygame.time.get_ticks()

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.creation_time
        remaining_time = self.duration - elapsed_time

        if remaining_time > 0:
            alpha = int(remaining_time / self.duration * 255)
            text_surface = self.font.render(self.text, True, self.color)
            text_surface.set_alpha(alpha)

            outline_surface = self.font.render(self.text, True, self.outline_color)
            outline_surface.set_alpha(alpha)

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx != 0 or dy != 0:
                        screen.blit(outline_surface, (((self.x - text_surface.get_width() // 2) + dx) * self.x_scale_rate, ((self.y - text_surface.get_height() // 2) + dy) * self.y_scale_rate))
                        
            screen.blit(text_surface, ((self.x - text_surface.get_width() // 2) * self.x_scale_rate, (self.y - text_surface.get_height() // 2) * self.y_scale_rate))
            return True
        return False
    
    def scale_parameters(self, x_scale_rate, y_scale_rate):
        self.x_scale_rate = x_scale_rate
        self.y_scale_rate = y_scale_rate

        self.font = pygame.font.Font(None, int(50 * x_scale_rate))