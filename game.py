import pygame
from pygame.locals import *
from map import Map 
from menu import Menu
from enemies.enemy import Enemy
from towers.archer_tower import ArcherTower
from towers.magic_tower import MagicTower
# from editor import Editor
# from debug import Debug


class Game():
    def __init__(self, screen):
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        
        self.screen = screen
        self.width, self.height = screen.get_width(), screen.get_height()
        
        self.game_map = Map(self.screen)
        self.menu = Menu(self.screen)

        self.money = 10000
        self.points = 0
        self.hearts = 3
        self.wave = 0

        self.game_pause = True

        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group() 
        self.path_collisions = pygame.sprite.Group()
        self.other_obstacles_collisions = pygame.sprite.Group()

        self.spawn_interval = 700 
        self.last_spawn_time = 0
        self.enemies_to_generate = 15
        self.drag_object = None

        
        self.load_rects("environment/path", self.path_collisions)
        self.load_rects("environment/others", self.other_obstacles_collisions)

        # # Editor related
        # editor = [Editor(screen, "environment/path"),
        #           Editor(screen, "environment/others")]
        # edit_mode = False

        # # Debug related
        # debug = Debug(screen)
        # debug_mode = False

    def load_rectangles_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                rectangles = []
                for line in file:
                    rect_x, rect_y, rect_width, rect_height = map(int, line.strip().split())
                    rectangles.append((rect_x, rect_y, rect_width, rect_height))
        except FileNotFoundError:
            print(f"File '{filename}' not found. No rectangles loaded.")
        
        return rectangles
    
    # Loads rectangles from file and adds them to group
    def load_rects(self, filename, group):

        rectangles = self.load_rectangles_from_file(filename)
        
        for rectangle in rectangles:
            rect_sprite = pygame.sprite.Sprite()
            rect_sprite.rect = pygame.Rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3])

            group.add(rect_sprite)


    def drag_object_conflict(self):

        return (pygame.sprite.spritecollide(self.drag_object, self.towers, False) or 
                pygame.sprite.spritecollide(self.drag_object, self.path_collisions, False) or
                pygame.sprite.spritecollide(self.drag_object, self.other_obstacles_collisions, False))  

    def draw_enemies_and_towers(self):
        
        sprites = self.enemies.sprites() + self.towers.sprites()
        
        for sprite in sorted(sprites, key=lambda s: s.y):
            sprite.draw(self.screen)

    # Images and effects that have to appear on top of everything else
    def draw_on_top(self):
        
        sprites = self.enemies.sprites() + self.towers.sprites()
        
        for sprite in sprites:
            sprite.draw_on_top(self.screen)

    def update_screen(self):
        self.menu.draw_all_menu(self.points, self.money, self.hearts, self.wave)
        self.game_map.draw_background()
        self.draw_enemies_and_towers()
        self.draw_on_top()
        
    
        if self.drag_object:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()

            self.drag_object.rect.center = (mouse_x, mouse_y)

            color = (0, 0, 255, 100)
            if self.drag_object_conflict():
                color = (255, 0, 0, 100)
            
            surface = pygame.Surface((160, 160), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, color, (80, 80), 80, 0)
            self.screen.blit(surface, (mouse_x - 80, mouse_y - 80))

            self.screen.blit(self.drag_object.image, (mouse_x - 80, mouse_y - 120))
        
    def update_game(self):
        self.towers.update(self.game_pause, self.enemies, self.screen)
        self.enemies.update(self.game_pause)
        

        if not self.game_pause:
            self.check_all_enemies()

            current_time = pygame.time.get_ticks()
            if self.enemies_to_generate > 0 and current_time - self.last_spawn_time >= self.spawn_interval:
                self.enemies.add(Enemy())

                self.enemies_to_generate -= 1
                self.last_spawn_time = current_time

    def check_all_enemies(self):
        enemies_on_end =[]
        killed_enemies = []

        for monster in self.enemies:
            is_killed, reward = monster.is_killed()
            if is_killed:
                killed_enemies.append((monster, reward))
                continue

            if monster.to_delete():
                enemies_on_end.append(monster)


        for monster_to_delete, reward in killed_enemies:
            self.enemies.remove(monster_to_delete)
            self.money += reward
            self.points += 200

        for monster_to_delete in enemies_on_end:
            self.enemies.remove(monster_to_delete)
            self.points -= 500
            self.money -= 100
            self.hearts -= 1

            if self.hearts <= 0:
                self.game_pause = True
                # TODO: end game

    def run(self):
        selected_tower = None
        new_tower_cost = 0
        drag_object_name = None
    
        running = True
        while running:
            self.update_screen()

            # if debug_mode:
            #     debug.draw_path_collisions_rect(path_collisions)
            #     debug.draw_others_rect(others)
            #     debug.draw_enemy_rect(enemies)
            #     if drag_object:
            #         debug.draw_drag_object_rect(drag_object)

            # if edit_mode:
            #     editor[1].edit()
            #     pygame.display.flip() # Required by editor
            #     continue

            self.update_game()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_position = pygame.mouse.get_pos()
                        # print(clicked_position)

                        if not self.drag_object:
                            if selected_tower:
                                selected_tower.selected = False
                                selected_tower = None

                            if self.menu.rect.collidepoint(clicked_position):
                                self.drag_object, drag_object_name, new_tower_cost = self.menu.handle_click(clicked_position)
                                
                                if not self.drag_object:
                                    if drag_object_name == "play":
                                        self.game_pause = False
                                    elif drag_object_name == "stop":
                                        self.game_pause = True

                                    continue


                                temp_sprite = pygame.sprite.Sprite()
                                temp_sprite.image = self.drag_object
                                temp_sprite.rect = pygame.rect.Rect(clicked_position[0], clicked_position[1], 50, 50)
                                self.drag_object = temp_sprite
                                

                            for tower in self.towers:
                                if tower.click(clicked_position[0], clicked_position[1]):
                                    selected_tower = tower
                                    break

                        elif self.drag_object and not self.drag_object_conflict():

                            if self.money - new_tower_cost < 0:
                                self.drag_object = None
                                drag_object_name = None
                                new_tower_cost = 0
                                # TODO: inform about not enought amount of money
                                continue

                            match drag_object_name:
                                case "archer":
                                    tower = ArcherTower(clicked_position[0]-3, clicked_position[1]-42)
                                    self.money -= new_tower_cost

                                case "magic":
                                    tower = MagicTower(clicked_position[0]-3, clicked_position[1]-42)
                                    self.money -= new_tower_cost

                            self.towers.add(tower)
                            self.drag_object = None


                    elif event.button == 3:
                        if selected_tower:
                                selected_tower.selected = False
                                selected_tower = None

                        self.drag_object = None
                        drag_object_name = None
                        new_tower_cost = 0

            pygame.display.flip()
   
            self.fpsClock.tick(self.fps)

