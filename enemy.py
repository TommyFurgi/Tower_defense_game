import pygame, math
from PIL import Image
from directions import Direction
import random

class Enemy():
    def __init__(self):
        self.x = 510
        self.y = 850
        
        self.speed = 0.7
        self.health = 300
        self.max_health = 300

        path =  [(520, 790), (530, 750), (550, 725), (580, 680), (600, 660), (640, 650), (660, 645), (680, 620), (695, 585), (700, 565), (695, 540), (686, 525), (683, 495), (678, 460),
                  (660, 445), (635, 440), (610, 430), (580, 420), (570, 410),  (560, 400), (550, 390), (525, 380), (505, 370), (480, 360), (460, 335), (455, 320), (450, 300), (452, 285), (455, 265), 
                  (470, 250), (485, 230), (500, 210), (515, 200), (530, 180), (1350, 175)]
        
        self.path = [(self.x, self.y)] + path
        self.animation_count = random.randint(0, 7) * 20
        self.path_pos = 0

        self.imgs_up = []
        self.imgs_down = []
        self.imgs_right = []
        self.imgs_left = []
        animation_strip = Image.open("img/enemy.png")
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

    def draw_health_bar(self, screen):
        length = 80
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(screen, (255,0,0), (self.x-42, self.y-75, length, 10), 0)
        pygame.draw.rect(screen, (0, 255, 0), (self.x-42, self.y - 75, health_bar, 10), 0)

    def draw(self, screen):
        match self.direction:
            case Direction.UP:
                self.img = self.imgs_up[self.animation_count//20]
            case Direction.DOWN:
                self.img = self.imgs_down[self.animation_count//20]
            case Direction.RIGHT:
                self.img = self.imgs_right[self.animation_count//20]
            case Direction.LEFT:
                self.img = self.imgs_left[self.animation_count//20]            

        screen.blit(self.img, (self.x - self.img.get_width()/2, self.y- self.img.get_height()/2 ))
        self.draw_health_bar(screen)
        

    def move(self):

        self.animation_count += 1
        if self.animation_count >= len(self.imgs_up) * 20:
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            return False
        else:
            x2, y2 = self.path[self.path_pos+1]

        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)
        dirn = (dirn[0] * self.speed, dirn[1] * self.speed)


        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.x = move_x
        self.y = move_y

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

        return True