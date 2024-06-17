from enemies.enemy import Enemy
import pygame
from directions import Direction
from effects.boost_effect import BoostEffect
import random
from source_manager import SourceManager

class EnemyBoss(Enemy):
    '''
    A subclass representing a boss type of enemy in the game.
    Inherits from the Enemy class and adds specific behavior and attributes.
    '''
    def __init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff):
        '''
        Initializes an instance of EnemyBoss with specific scaling rates and differences.

        Args:
            x_scale_rate (float): Scaling rate for the x-axis.
            y_scale_rate (float): Scaling rate for the y-axis.
            x_scale_diff (float): Scaling difference for the x-axis.
            y_scale_diff (float): Scaling difference for the y-axis.
        '''
        self.path = SourceManager.get_path("default")

        Enemy.__init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff)
        self.load_images("boss")

        self.speed = 1
        self.max_speed = 1.1
        self.health = 400
        self.max_health = 400
        self.reward = 50

    def load_images(self, images_filename):
        '''
        Loads and initializes the animation frames for the EnemyBoss based on an image strip.

        Args:
            images_filename (str): The filename of the image strip containing animation frames.
        '''
        self.animation_count = random.randint(0, 2) * 10
        
        self.path_pos = 0
        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []
        
        animation_strip = SourceManager.get_image(images_filename)
        frame_width = 120
        frame_height = 120
        
        for i in range(1,4):
            for j in range(1,4):
                frame = animation_strip.crop((frame_width * j, frame_height * i + 40, frame_width * (j + 1), frame_height * (i+1) + 40))

                data = frame.tobytes()
                pygame_surface = pygame.image.fromstring(data, frame.size, "RGBA").convert_alpha()

                match i:
                    case 1:
                        self.imgs_right.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                        pygame_surface_flipped = pygame.transform.flip(pygame_surface, True, False)
                        self.imgs_left.append(pygame.transform.scale(pygame_surface_flipped, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())

                    case 2:
                        self.imgs_up.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 3:
                        self.imgs_down.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())

                self.original_sized_images[i].append(pygame_surface)

        self.direction = Direction.RIGHT
        self.img = self.imgs_right[0]

        self.flipped = False

    def update(self, game_pause, enemies):
        '''
        Updates the state of the EnemyBoss during gameplay, including handling special behaviors.

        Args:
            game_pause (bool): Flag indicating whether the game is paused.
            enemies (pygame.sprite.Group): Group of all enemies in the game.
        '''
        super().update(game_pause, enemies)
        self.find_enemies_around(enemies)

    def find_enemies_around(self, enemies):
        '''
        Detects and boosts nearby enemies when the EnemyBoss collides with them.

        Args:
            enemies (pygame.sprite.Group): Group of all enemies in the game.
        '''
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        for enemy in enemies_collision:
            # Bosses can not boost each other
            if not isinstance(enemy, EnemyBoss):
                enemy.add_effect(BoostEffect(1.6, 3))

    def scale_parameters(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff):
        '''
        Scales the parameters of the EnemyBoss instance based on given scaling factors and differences.

        Args:
            x_scale_rate (float): The scaling factor for the x-axis.
            y_scale_rate (float): The scaling factor for the y-axis.
            x_scale_diff (float): The scaling difference for the x-axis.
            y_scale_diff (float): The scaling difference for the y-axis.
        '''
        super().scale_parameters(x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff)

        for i in range(1, 4):
            for j, img in enumerate(self.original_sized_images[i]):
                match i:
                    case 1:
                        self.imgs_right[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
                        pygame_surface_flipped = pygame.transform.flip(img, True, False)
                        self.imgs_left[j] = pygame.transform.scale(pygame_surface_flipped, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
                    case 2:
                        self.imgs_up[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
                    case 3:
                        self.imgs_down[j] = pygame.transform.scale(img, (128 * x_scale_rate, 128 * y_scale_rate)).convert_alpha()
