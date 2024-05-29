from enemies.enemy import Enemy
import pygame
from directions import Direction
import random
from source_manager import SourceManager
from effects.effect_type import EffectType


class EnemyBasic(Enemy):
    def __init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff):
        self.path = [
            (540, 900), (539, 892), (541, 868), (543, 837), (547, 806), (555, 771),
            (570, 750), (587, 732), (607, 717), (632, 706), (659, 699), (677, 693),
            (692, 667), (699, 638), (702, 597), (695, 569), (688, 544), (676, 530),
            (660, 515), (646, 503), (627, 496), (606, 493), (574, 479), (550, 470),
            (523, 457), (501, 429), (481, 409), (472, 383), (470, 354), (462, 319),
            (467, 289), (475, 263), (487, 240), (503, 229), (525, 214), (547, 207),
            (573, 205), (595, 204), (615, 201), (637, 200), (680, 199), (717, 197),
            (752, 198), (787, 197), (816, 198), (853, 199), (895, 195), (935, 194),
            (979, 193), (1019, 194), (1055, 193), (1098, 191), (1147, 192),
            (1195, 190), (1246, 191), (1289, 190), (1329, 191), (1353, 192)
        ]

        Enemy.__init__(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff)
        self.load_images("enemy")
        
        self.speed = 1.2
        self.max_speed = 1.2
        self.health = 200
        self.max_health = 200
        self.reward = 30
        
        self.effects_resistance[EffectType.POISON] = True # Cannot be poisoned
    

    def load_images(self, images_filename):
        self.animation_count = random.randint(0, 7) * 10
        self.path_pos = 0
        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []

        animation_strip = SourceManager.get_image(images_filename)
        frame_width = 64
        frame_height = 64
        
        for i in range(4):
            for j in range(1,9):
                frame = animation_strip.crop((frame_width * j, frame_height * i, frame_width * (j + 1), frame_height * (i+1)))

                data = frame.tobytes()
                pygame_surface = pygame.image.fromstring(data, frame.size, "RGBA")

                match i:
                    case 0:
                        self.imgs_up.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 1:
                        self.imgs_left.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 2:
                        self.imgs_down.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())
                    case 3:
                        self.imgs_right.append(pygame.transform.scale(pygame_surface, (128 * self.x_scale_rate, 128 * self.y_scale_rate)).convert_alpha())

                self.original_sized_images[i].append(pygame_surface)

        self.direction = Direction.RIGHT
        self.img = self.imgs_right[0]

        self.flipped = False


    def scale_parameters(self, x_scale_rate, y_scale_rate, x_scale_diff, y_scale_diff):
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
    