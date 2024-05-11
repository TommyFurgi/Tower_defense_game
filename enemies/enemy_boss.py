from enemies.enemy import Enemy
import pygame
from PIL import Image
from directions import Direction
from effects.effect_type import EffectType
from effects.boost_effect import BoostEffect
import random

class EnemyBoss(Enemy):
    
    def __init__(self):
        Enemy.__init__(self, "assets/enemies/boss.png")

        # starting point
        self.x = 540
        self.y = 900
        self.rect = pygame.Rect(self.x, self.y, 64, 64) # Required in order for collisions to work

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
        self.speed = 1
        self.max_speed = 1.1
        self.health = 400
        self.max_health = 400
        self.reward = 50

        
    def load_images(self, images_filename):
        
        self.animation_count = random.randint(0, 2) * 10
        
        self.path_pos = 0
        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []
        
        animation_strip = Image.open(images_filename)
        frame_width = 120
        frame_height = 120
        
        for i in range(1,4):
            for j in range(1,4):
                frame = animation_strip.crop((frame_width * j, frame_height * i + 40, frame_width * (j + 1), frame_height * (i+1) + 40))

                data = frame.tobytes()
                pygame_surface = pygame.image.fromstring(data, frame.size, "RGBA")

                match i:
                    case 1:
                        self.imgs_right.append(pygame.transform.scale(pygame_surface, (128, 128)))
                        pygame_surface_flipped = pygame.transform.flip(pygame_surface, True, False)
                        self.imgs_left.append(pygame.transform.scale(pygame_surface_flipped, (128, 128)))

                    case 2:
                        self.imgs_up.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 3:
                        self.imgs_down.append(pygame.transform.scale(pygame_surface, (128, 128)))

        self.direction = Direction.RIGHT
        self.img = self.imgs_right[0]

        self.flipped = False



    def handle_effects(self):
        
        for effect in self.effects:
            
            effect_type, property, color = effect.update()
            self.speed = self.max_speed

            
            match effect_type:
                case EffectType.POISION:
                    self.lose_hp(property, color)
                    #TODO: poison visual effect
                case EffectType.SLOWDOWN:
                    #TODO: visual effect
                    self.speed = property * self.max_speed
                case EffectType.BOOST:
                    pass
                case EffectType.EFFECT_FINISHED: # effect duration has ended
                    pass


    def update(self, game_pause, enemies):
        if not game_pause:
            self.move()
            self.find_enemies_around(enemies)
            self.handle_effects()


    def find_enemies_around(self, enemies):
        enemies_collision = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_circle)

        for enemy in enemies_collision:
            # Bosses can not boost each other
            if not isinstance(enemy, EnemyBoss):
                enemy.add_effect(BoostEffect(1.6, 3))


    def add_effect(self, new_effect):
    
        # Enemy should only have one effect of given type at a time

        for effect in self.effects:
            
            if effect.get_effect_type() == new_effect.get_effect_type():
                self.effects.remove(effect)
                break
        
        self.effects.add(new_effect)