from enemies.enemy import Enemy
import pygame
from directions import Direction
import random
from resource_manager import ResourceManager
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
        super().__init__(x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff, "alternative")
        self.original_sized_images = ResourceManager.get_image("magic")
        self.imgs_up, self.imgs_left, self.imgs_down, self.imgs_right = tuple(self.original_sized_images)

        self.speed = 1.5
        self.max_speed = 1.5
        self.health = 300
        self.max_health = 300
        self.reward = 20

        self.effects_resistance[EffectType.SLOWDOWN] = True  # Cannot be slowed down
        self.animation_count = random.randint(0, 7) * 10

        if x_scale_rate != 1 or y_scale_rate != 1:
            self.scale_parameters(x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff, True)

    def scale_parameters(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff, initialize_enemy = False):
        '''
        Scales the parameters of the EnemyMagic instance based on given scaling factors and differences.

        Args:
            x_scale_rate (float): The scaling factor for the x-axis.
            y_scale_rate (float): The scaling factor for the y-axis.
            x_scale_diff (float): The scaling difference for the x-axis.
            y_scale_diff (float): The scaling difference for the y-axis.
            initialize_enemy (bool): The flag indicating whether the function is called during initialization
        '''
        super().scale_parameters(x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff, initialize_enemy)

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