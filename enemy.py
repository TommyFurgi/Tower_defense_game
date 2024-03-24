import pygame, math
from PIL import Image
from directions import Direction

class Enemy():
    def __init__(self, screen):
        self.x = 510
        self.y = 850
        
        self.speed = 1.3
        self.health = 300

        path =  [(520, 790), (530, 750), (550, 725), (580, 680), (600, 660), (640, 650), (660, 645), (680, 620), (695, 585), (700, 565), (695, 540), (686, 525), (683, 495), (678, 460),
                  (660, 445), (635, 440), (610, 430), (590, 415), (570, 400), (550, 385), (535, 360), (515, 340), (500, 325), (495, 305), (490, 290), (485, 270), (490, 255), (510, 230),
                  (525, 205), (540, 182), (560, 173), (585, 171), (615, 170), (640, 166)] # ...
        
        self.path = [(self.x, self.y)] + path
        self.animation_count = 0
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


    def draw(self, screen):
        match self.direction:
            case Direction.UP:
                self.img = self.imgs_up[self.animation_count//10]
            case Direction.DOWN:
                self.img = self.imgs_down[self.animation_count//10]
            case Direction.RIGHT:
                self.img = self.imgs_right[self.animation_count//10]
            case Direction.LEFT:
                self.img = self.imgs_left[self.animation_count//10]            

        screen.blit(self.img, (self.x - self.img.get_width()/2, self.y- self.img.get_height()/2 ))
        

    def move(self):

        self.animation_count += 1
        if self.animation_count >= len(self.imgs_up) * 10:
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path): # TODO !!!
            return
            x2, y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.path_pos+1]


        # print(x2,y2)

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