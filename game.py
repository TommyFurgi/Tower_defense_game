import pygame
from pygame.locals import *
from map import Map 
from menu import Menu
from main_menu import Main_menu
from towers.archer_tower import ArcherTower
from towers.magic_tower import MagicTower
from towers.cannon_tower import CannonTower
from waves.wave_manager import WaveManager
from source_manager import SourceManager
from text_alert import TextAlert
# from editor import Editor
# from debug import Debug


class Game():
    def __init__(self, screen):
        #self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.time_scale = 1
        self.delta_time = self.fpsClock.get_time() * self.time_scale # time since last frame multiplied by time scale (eg. timescale = 2 => 2x speed)
        
        self.screen = screen
        self.width, self.height = screen.get_width(), screen.get_height()
        
        self.game_map = Map(self.screen)
        self.menu = Menu(self.screen)
        self.main_menu = Main_menu(self.screen)

        self.money = 800
        self.points = 0
        self.hearts = 3
        self.wave = 1

        self.game_pause = True
        self.game_running = False
        self.player_won = True
        self.show_main_menu = True
        self.end_game = False

        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group() 
        self.path_collisions = pygame.sprite.Group()
        self.other_obstacles_collisions = pygame.sprite.Group()

        self.drag_object = None
        self.sound_play = True
         
        self.sped_up = False
        
        self.text_alerts = set()
        
        self.wave_manager = WaveManager()
        self.current_wave = self.wave_manager.get_next_wave()
        
        self.load_rects("path", self.path_collisions)
        self.load_rects("others", self.other_obstacles_collisions)

        self.background_music = SourceManager.get_sound("music")

        # # Editor related
        # editor = [Editor(screen, "environment/path"),
        #           Editor(screen, "environment/others")]
        # edit_mode = False

        # # Debug related
        # debug = Debug(screen)
        # debug_mode = False
    

    # Loads rectangles from file and adds them to group
    def load_rects(self, name, group):
        rectangles = SourceManager.get_rectangles(name)
        
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
            sprite.draw(self.screen, self.delta_time)


    # Images and effects that have to appear on top of everything else
    def draw_on_top(self):
        sprites = self.towers.sprites()
        
        for sprite in sprites:
            sprite.draw_on_top(self.screen, self.delta_time)


    def update_screen(self):
        self.menu.draw_all_menu(self.points, self.money, self.hearts, self.wave, self.game_pause)
        self.game_map.draw_background()
        self.draw_enemies_and_towers()
        self.draw_on_top()
        self.draw_text_alerts()
        
    
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

        if self.show_main_menu:
            if self.end_game:
                self.main_menu.draw_end_menu(self.screen, self.player_won, self.points)
            else:
                self.main_menu.draw_start_menu(self.screen, self.game_running)

    
    def spawn_enemies(self):
        if self.current_wave.has_next_enemy():
            
            new_enemy = self.current_wave.get_next_enemy()

            if new_enemy:
                self.enemies.add(new_enemy)
                
        elif len(self.enemies) == 0 and self.end_game == False: # All enemies were killed
            self.game_pause = True
            self.text_alerts.add(TextAlert("Wave " + str(self.wave) + " completed!", 2000, (0, 255, 0)))

            if self.wave_manager.has_next_wave(): # There is a next wave
                self.current_wave = self.wave_manager.get_next_wave()
                self.wave += 1
            else: # All enemies killed and no next wave
                self.player_won = True
                self.end_game = True
                self.show_main_menu = True
                self.game_running = False        
        

    def update_game(self):
        self.towers.update(self.game_pause, self.enemies, self.screen, self.delta_time)
        self.enemies.update(self.game_pause, self.enemies, self.delta_time)
        
        if not self.game_pause:
            self.check_all_enemies()
            self.spawn_enemies()


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
                self.game_running = False
                self.player_won = False
                self.end_game = True
                self.show_main_menu = True
                self.text_alerts.add(TextAlert("Game over!", 2000, (255, 0, 0)))


    def handle_restart_game(self): 
        self.money = 800
        self.points = 0
        self.hearts = 3
        self.wave = 1

        self.game_pause = True

        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group() 

        self.drag_object = None                                
        self.sped_up = False
        
        self.wave_manager = WaveManager()
        self.current_wave = self.wave_manager.get_next_wave()

        self.player_won = False
        self.game_running = True
        self.show_main_menu = False
        self.end_game = False

    def draw_text_alerts(self):
        
        alerts_to_delete = []
        
        for text_alert in self.text_alerts:
            if not text_alert.draw(self.screen):
                alerts_to_delete.append(text_alert)
                
        for alert in alerts_to_delete:
            self.text_alerts.remove(alert)

    def run(self):
        selected_tower = None
        new_tower_cost = 0
        drag_object_name = None
    
        running = True
        while running:
            self.update_screen()

            if self.show_main_menu:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False

                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            clicked_position = pygame.mouse.get_pos()

                            match self.main_menu.handle_click_action(clicked_position, self.end_game, self.game_running):
                                case "music":
                                    if self.sound_play:
                                        self.sound_play = False
                                        self.background_music.set_volume(0)
                                    else:
                                        self.sound_play = True
                                        self.background_music.set_volume(0.015)
                                case "new_game":
                                    self.handle_restart_game()
                                    selected_tower = None
                                    drag_object_name = None
                                case "countinue":
                                    self.show_main_menu = False
                                case "back_to_menu":
                                    self.end_game = False
                                    selected_tower = None
                                    drag_object_name = None
                                case _:
                                    pass 
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and self.game_running:
                            self.show_main_menu = False

            else:    

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
                                    value = selected_tower.manage_tower_action(clicked_position, self.money, self.text_alerts)

                                    self.money += value
                                    if value >= 0: 
                                        if value > 0: # tower sold
                                            self.towers.remove(selected_tower)

                                        selected_tower.selected = False
                                        selected_tower = None
                                        
                                        
                                if self.menu.rect.collidepoint(clicked_position):
                                    self.drag_object, drag_object_name, new_tower_cost = self.menu.handle_click(clicked_position, self.game_pause)
                                    
                                    if not self.drag_object:
                                        if drag_object_name == "play":
                                            self.game_pause = False
                                            self.current_wave.reset_spawn_time()
                                            for enemy in self.enemies:
                                                enemy.unpause_effects()

                                        elif drag_object_name == "stop":
                                            self.game_pause = True
                                            self.current_wave.pause_spawn_time()
                                            for enemy in self.enemies:
                                                enemy.pause_effects()

                                        elif drag_object_name == "speed_up":
                                            if self.sped_up:
                                                self.fps = 60
                                                self.sped_up = False
                                            else:
                                                self.fps = 120
                                                self.sped_up = True

                                        elif drag_object_name == "music":
                                            if self.sound_play:
                                                self.sound_play = False
                                                self.background_music.set_volume(0)
                                            else:
                                                self.sound_play = True
                                                self.background_music.set_volume(0.015)

                                        continue


                                    temp_sprite = pygame.sprite.Sprite()
                                    temp_sprite.image = self.drag_object
                                    temp_sprite.rect = pygame.rect.Rect(clicked_position[0], clicked_position[1], 50, 50)
                                    self.drag_object = temp_sprite
                                    

                                for tower in self.towers:
                                    if tower.select_tower(clicked_position[0], clicked_position[1]):
                                        selected_tower = tower
                                        break

                            elif self.drag_object:
                                
                                if not self.drag_object_conflict():
                                
                                    if self.money - new_tower_cost < 0:
                                        self.drag_object = None
                                        drag_object_name = None
                                        new_tower_cost = 0
                                        self.text_alerts.add(TextAlert("Not enough money!", 1000, (255, 0, 0)))
                                        continue

                                    match drag_object_name:
                                        case "archer":
                                            tower = ArcherTower(clicked_position[0]-3, clicked_position[1]-42)
                                            self.money -= new_tower_cost

                                        case "magic":
                                            tower = MagicTower(clicked_position[0]-3, clicked_position[1]-42)
                                            self.money -= new_tower_cost
                                            
                                        case "cannon":
                                            tower = CannonTower(clicked_position[0]-3, clicked_position[1]-42)
                                            self.money -= new_tower_cost

                                    self.towers.add(tower)
                                    self.drag_object = None
                                    
                                else:
                                    
                                    self.text_alerts.add(TextAlert("Can't place a tower here!", 2000, (255, 0, 0)))


                        elif event.button == 3:
                            if selected_tower:
                                    selected_tower.selected = False
                                    selected_tower = None

                            self.drag_object = None
                            drag_object_name = None
                            new_tower_cost = 0

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.show_main_menu = True

            pygame.display.flip()
   
            self.fpsClock.tick()
            self.delta_time = self.fpsClock.get_time() * self.time_scale
            
            #print("fps: ", self.fpsClock.get_fps())

