from enemies.enemy import Enemy
import pygame
from directions import Direction
import random
from source_manager import SourceManager
from effects.effect_type import EffectType

class EnemyMagic(Enemy):
    '''
    A subclass representing a magical type of enemy in the game.
    Inherits from the Enemy class and adds specific behavior and attributes.
    '''
    def __init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff):
        '''
        Initializes an instance of EnemyMagic with specific scaling rates and differences.

        Args:
            x_scale_rate (float): Scaling rate for the x-axis.
            y_scale_rate (float): Scaling rate for the y-axis.
            x_scale_diff (float): Scaling difference for the x-axis.
            y_scale_diff (float): Scaling difference for the y-axis.
        '''
        self.path = SourceManager.get_path("alternative")

        Enemy.__init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff)
        self.load_images("enemy")

        self.speed = 1.5
        self.max_speed = 1.5
        self.health = 300
        self.max_health = 300
        self.reward = 20

        self.effects_resistance[EffectType.SLOWDOWN] = True  # Cannot be slowed down

    def load_images(self, images_filename):
        '''
        Loads and initializes the animation frames for the EnemyMagic based on an image strip.

        Args:
            images_filename (str): The filename of the image strip containing animation frames.
        '''
        self.animation_count = random.randint(0, 7) * 10
        self.path_pos = 0
        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []
        
        animation_strip = SourceManager.get_image(images_filename)
        frame_width = 64
        frame_height = 64
        
        for i in range(4,8):
            for j in range(1,9):
                frame = animation_strip.crop((frame_width * j, frame_height * i, frame_width * (j + 1), frame_height * (i+1)))

                data = frame.tobytes()
                pygame_surface = pygame.image.fromstring(data, frame.size, "RGBA").convert_alpha()

                match i:
                    case 4:
                        self.imgs_up.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 5:
                        self.imgs_left.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 6:
                        self.imgs_down.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 7:
                        self.imgs_right.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())

                self.original_sized_images[i-4].append(pygame_surface)

        self.direction = Direction.RIGHT
        self.img = self.imgs_right[0]

        self.flipped = False

    def scale_parameters(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff):
        '''
        Scales the parameters of the EnemyMagic instance based on given scaling factors and differences.

        Args:
            x_scale_rate (float): The scaling factor for the x-axis.
            y_scale_rate (float): The scaling factor for the y-axis.
            x_scale_diff (float): The scaling difference for the x-axis.
            y_scale_diff (float): The scaling difference for the y-axis.
        '''
        super().scale_parameters(x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff)

        for i in range(4):
            for j, img in enumerate(self.original_sized_images[i]):
                match i:
                    case 0:
                        self.imgs_up[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
                    case 1:
                        self.imgs_left[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
                    case 2:
                        self.imgs_down[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
                    case 3:
                        self.imgs_right[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()