from enemies.enemy import Enemy
import pygame
from PIL import Image
from directions import Direction
from effects.effect_type import EffectType
import random

class EnemyMagic(Enemy):
    
    def __init__(self):
        Enemy.__init__(self, "assets/enemies/enemy.png")

        # starting point
        self.x = 1349
        self.y = 755
        self.rect = pygame.Rect(self.x, self.y, 64, 64) # Required in order for collisions to work
        
        self.path = [
            (1349, 755), (1305, 755), (1268, 755), (1238, 754), (1202, 756),
            (1167, 756), (1121, 757), (1077, 758), (1038, 757), (999, 756),
            (972, 758), (940, 759), (888, 759), (845, 758), (802, 750),
            (773, 734), (742, 719), (722, 701), (704, 663), (697, 627),
            (685, 581), (666, 544), (645, 505), (594, 477), (549, 469),
            (511, 456), (494, 426), (479, 401), (471, 345), (467, 293),
            (494, 232), (555, 207), (606, 196), (685, 192), (736, 192),
            (798, 187), (872, 195), (912, 197), (963, 195), (1003, 195),
            (1052, 193), (1102, 193), (1158, 194), (1209, 196), (1253, 194),
            (1288, 193), (1324, 190), (1353, 187), (1381, 185)
        ]

        self.speed = 1.5
        self.max_speed = 1.5
        self.health = 300
        self.max_health = 300
        self.reward = 20

        

    
    def load_images(self, images_filename):
        
        self.animation_count = random.randint(0, 7) * 10
        self.path_pos = 0
        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []
        
        animation_strip = Image.open(images_filename)
        frame_width = 64
        frame_height = 64
        
        for i in range(4,8):
            for j in range(1,9):
                frame = animation_strip.crop((frame_width * j, frame_height * i, frame_width * (j + 1), frame_height * (i+1)))

                data = frame.tobytes()
                pygame_surface = pygame.image.fromstring(data, frame.size, "RGBA")

                match i:
                    case 4:
                        self.imgs_up.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 5:
                        self.imgs_left.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 6:
                        self.imgs_down.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 7:
                        self.imgs_right.append(pygame.transform.scale(pygame_surface, (128, 128)))

        self.direction = Direction.RIGHT
        self.img = self.imgs_right[0]

        self.flipped = False

    def handle_effects(self):
        
        finished_effects = []
        
        for effect in self.effects:
            
            effect_type, property = effect.update()
            
            match effect_type:
                case EffectType.POISION:
                    self.lose_hp(property)
                    #TODO: poison visual effect
                case EffectType.SLOWDOWN:
                    # can not be slowed down
                    pass
                case EffectType.EFFECT_FINISHED: # effect duration has ended
                    finished_effects.append(effect)
                    
        for finished_effect in finished_effects:
            
            match finished_effect.get_effect_type():
                
                case EffectType.SLOWDOWN:
                    self.speed = self.max_speed # restoring speed to its original value
            
            self.effects.remove(finished_effect)