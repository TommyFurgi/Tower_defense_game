import pygame, math
from PIL import Image
from directions import Direction
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen):

        pygame.sprite.Sprite.__init__(self)

        self.x = 540
        self.y = 900
        
        self.rect = pygame.Rect(self.x, self.y, 64, 64) # Required in order for collisions to work
        
        self.speed = 1.5
        self.health = 300
        self.max_health = 300
        self.reached_last_point = False
        self.reward = 200
        
        self.path = [(self.x, self.y)] + [
                (539, 892), (541, 868), (543, 837), (547, 806), (555, 771),
                (570, 750), (587, 732), (607, 717), (632, 706), (659, 699),
                (677, 693), (692, 667), (699, 638), (702, 597), (695, 569),
                (688, 544), (676, 530), (660, 515), (646, 503), (627, 496),
                (606, 493), (574, 479), (550, 470), (523, 457), (501, 429),
                (481, 409), (472, 383), (470, 354), (462, 319), (467, 289),
                (475, 263), (487, 240), (503, 229), (525, 214), (547, 207),
                (573, 205), (595, 204), (615, 201), (637, 200), (680, 199),
                (717, 197), (752, 198), (787, 197), (816, 198), (853, 199),
                (895, 195), (935, 194), (979, 193), (1019, 194), (1055, 193),
                (1098, 191), (1147, 192), (1195, 190), (1246, 191), (1289, 190),
                (1329, 191), (1353, 192)
            ]
        
        self.animation_count = random.randint(0, 7) * 20
        self.path_pos = 0

        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []
        self.screen = screen
        animation_strip = Image.open("assets/enemies/enemy.png")
        frame_width = 64
        frame_height = 64
        
        for i in range(4):
            for j in range(1,9):
                frame = animation_strip.crop((frame_width * j, frame_height * i, frame_width * (j + 1), frame_height * (i+1)))

                data = frame.tobytes()
                pygame_surface = pygame.image.fromstring(data, frame.size, "RGBA")

                match i:
                    case 0:
                        self.imgs_up.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 1:
                        self.imgs_left.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 2:
                        self.imgs_down.append(pygame.transform.scale(pygame_surface, (128, 128)))
                    case 3:
                        self.imgs_right.append(pygame.transform.scale(pygame_surface, (128, 128)))

        
        self.direction = Direction.RIGHT
        self.img = self.imgs_right[0]

        self.flipped = False

    def draw_health_bar(self):
        length = 80
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(self.screen, (255,0,0), (self.x-42, self.y - 130, length, 10), 0)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x-42, self.y - 130, health_bar, 10), 0)

    def draw(self):
        match self.direction:
            case Direction.UP:
                self.img = self.imgs_up[self.animation_count//20]
            case Direction.DOWN:
                self.img = self.imgs_down[self.animation_count//20]
            case Direction.RIGHT:
                self.img = self.imgs_right[self.animation_count//20]
            case Direction.LEFT:
                self.img = self.imgs_left[self.animation_count//20]            

        self.screen.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height() ))
        self.draw_health_bar()
        

    def move(self):

        self.animation_count += 1
        if self.animation_count >= len(self.imgs_up) * 20:
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 < len(self.path):
            x2, y2 = self.path[self.path_pos+1]
        else:
            self.reached_last_point = True
            return
        
        if self.x > 1350:
            self.reached_last_point = True
            return

        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)
        dirn = (dirn[0] * self.speed, dirn[1] * self.speed)


        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.x = move_x
        self.y = move_y
        
        self.rect.center = (move_x, move_y)

        # Go to next point
        if dirn[0] >= 0: # moving right
            if dirn[1] >= 0: # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else: # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y <= y2:
                    self.path_pos += 1
 
        
        # Setting direction
        self.direction = Direction.set_direction(dirn)

        # return True
    
    def update(self, game_pause):
        if not game_pause:
            self.move()
            
        self.draw()

    def lose_hp(self, hp_lost):
        self.health -= hp_lost

    def to_delete(self):
        return self.reached_last_point
    
    def is_killed(self):
        if self.health <= 0:
            return True, self.reward
        
        return False, None
    
    def get_position(self):
        return self.x, self.y
        