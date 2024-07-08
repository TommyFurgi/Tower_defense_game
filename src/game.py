import pygame
from pygame.locals import *
from map import Map 
from shop import Shop
from main_menu import Main_menu
from towers.archer_tower import ArcherTower
from towers.magic_tower import MagicTower
from towers.cannon_tower import CannonTower
from waves.wave_manager import WaveManager
from resource_manager import ResourceManager
from text_alert import TextAlert
from math import sqrt

class Game():
    def __init__(self, screen):
        """
        Initialize the Tower Defense game.

        Args:
            screen (pygame.Surface): The main Pygame surface object representing the game screen.
        """
        self.x_scale_rate = 1
        self.y_scale_rate = 1

        self.x_scale_diff = 1
        self.y_scale_diff = 1

        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.time_scale = 1
        self.delta_time = self.fpsClock.get_time() * self.time_scale # time since last frame multiplied by time scale (eg. timescale = 2 => 2x speed)
        
        self.screen = screen
        self.width, self.height = screen.get_width(), screen.get_height()
        
        self.game_map = Map(self.screen)
        self.menu = Shop(self.screen)
        self.main_menu = Main_menu(self.screen)

        self.handle_restart_game()
        self.show_main_menu = True
        self.game_running = False

        self.path_collisions = pygame.sprite.Group()
        self.other_obstacles_collisions = pygame.sprite.Group()

        self.sound_play = True 
        self.text_alerts = set()
        
        self.load_rects("path", self.path_collisions)
        self.load_rects("others", self.other_obstacles_collisions)

        self.success_sound = ResourceManager.get_sound("success")
        self.failture_sound = ResourceManager.get_sound("failture")
        self.success_sound_end_game = ResourceManager.get_sound("success_end_game")
        self.building_sound = ResourceManager.get_sound("building")

        self.objects_to_scale = {self.game_map, self.menu, self.main_menu}

    # Loads rectangles from file and adds them to group
    def load_rects(self, name, group):
        """
        Load rectangles from a file using SourceManager and add them to a sprite group.

        Args:
            name (str): The name identifier for the rectangles to load from SourceManager.
            group (pygame.sprite.Group): The sprite group to which the loaded rectangles will be added.
        """
        rectangles = ResourceManager.get_rectangles(name)
        
        for rectangle in rectangles:
            rect_sprite = pygame.sprite.Sprite()
            rect_sprite.rect = pygame.Rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3])

            group.add(rect_sprite)


    def drag_object_conflict(self):
        """
        Check for collision conflicts with the currently dragged object.

        Returns:
            bool: True if there's a collision conflict, False otherwise.
        """
        return (pygame.sprite.spritecollide(self.drag_object, self.towers, False) or 
                pygame.sprite.spritecollide(self.drag_object, self.path_collisions, False) or
                pygame.sprite.spritecollide(self.drag_object, self.other_obstacles_collisions, False))  


    def draw_enemies_and_towers(self):
        """
        Draw enemies and towers on the game screen.
        """
        sprites = self.enemies.sprites() + self.towers.sprites()
        
        for sprite in sorted(sprites, key=lambda s: s.y):
            sprite.draw(self.screen, self.delta_time)

    # Images and effects that have to appear on top of everything else
    def draw_on_top(self):
        """
        Draw images and effects that need to appear on top of everything else on the screen.
        """
        sprites = self.towers.sprites()
        
        for sprite in sprites:
            sprite.draw_on_top(self.screen, self.delta_time)

    def update_screen(self):
        """
        Update the entire game screen with background, enemies, towers, menus, and text alerts.
        """
        self.game_map.draw_background()
        self.draw_enemies_and_towers()
        self.draw_on_top()
        self.menu.draw_all_menu(self.points, self.money, self.hearts, self.wave, self.game_pause)
        self.draw_text_alerts()
    
        if self.drag_object:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()

            self.drag_object.rect.center = (mouse_x, mouse_y)

            color = (0, 0, 255, 100)
            if self.drag_object_conflict():
                color = (255, 0, 0, 100)
            
            radius_rate = sqrt((self.x_scale_rate**2 + self.y_scale_rate**2)/2)

            surface = pygame.Surface((160 * self.x_scale_rate, 160 * self.y_scale_rate), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, color, (80 * self.x_scale_rate, 80 * self.y_scale_rate), 80 * radius_rate, 0)
            self.screen.blit(surface, (mouse_x - 80 * self.x_scale_rate, mouse_y - 80 * self.y_scale_rate))

            self.screen.blit(self.drag_object.image, (mouse_x - 80 * self.x_scale_rate, mouse_y - 120 * self.y_scale_rate))

        if self.show_main_menu:
            self.main_menu.draw_main_menu(self.screen, self.game_running, self.player_won, self.points)

    
    def spawn_enemies(self):
        """
        Spawn enemies on the game map according to the current wave configuration.
        """
        if self.current_wave.has_next_enemy():
            
            new_enemy = self.current_wave.get_next_enemy(self.x_scale_rate, self.y_scale_rate, self.x_scale_diff, self.y_scale_diff)

            if new_enemy:
                self.enemies.add(new_enemy)
                
        elif len(self.enemies) == 0 and self.end_game == False: # All enemies were killed
            self.game_pause = True
            self.text_alerts.add(TextAlert("Wave " + str(self.wave) + " completed!", 2000, (0, 255, 0), self.x_scale_rate, self.y_scale_rate))

            if self.wave_manager.has_next_wave(): # There is a next wave
                self.success_sound.play()
                self.current_wave = self.wave_manager.get_next_wave()
                self.wave += 1
            else: # All enemies killed and no next wave
                self.success_sound_end_game.play()
                self.player_won = True
                self.end_game = True
                self.show_main_menu = True
                self.game_running = False 
                self.main_menu.show_info = False       
        

    def update_game(self):
        """
        Update game logic including tower and enemy updates, collision checks, and game state management.
        """
        self.towers.update(self.game_pause, self.enemies, self.screen, self.delta_time)
        self.enemies.update(self.game_pause, self.enemies)
        
        if not self.game_pause:
            self.check_all_enemies()
            self.spawn_enemies()

    def check_all_enemies(self):
        """
        Check the status of all enemies on the game map, including whether they are killed or have reached the end.
        """
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
                self.failture_sound.play()
                self.game_pause = True
                self.game_running = False
                self.player_won = False
                self.end_game = True
                self.show_main_menu = True
                self.main_menu.show_info = False   
                self.text_alerts.add(TextAlert("Game over!", 2000, (255, 0, 0), self.x_scale_rate, self.y_scale_rate))

    def handle_restart_game(self):
        """
        Reset all game parameters and start a new game.
        """ 
        self.money = 1000
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

        self.player_won = None
        self.game_running = True
        self.show_main_menu = False
        self.end_game = False

    def draw_text_alerts(self):
        """
        Draw text alerts on the game screen and manage their lifecycle.
        """
        alerts_to_delete = []
        
        for text_alert in self.text_alerts:
            if not text_alert.draw(self.screen):
                alerts_to_delete.append(text_alert)
                
        for alert in alerts_to_delete:
            self.text_alerts.remove(alert)

    def scale_game(self, new_w, new_h):
        """
        Scale the entire game to fit a new window size.

        Args:
            new_w (int): The new width of the game window.
            new_h (int): The new height of the game window.
        """
        new_width = max(800, min(2400, new_w))
        new_height = max(450, min(1800, new_h))

        self.screen = pygame.display.set_mode((new_width, new_height), pygame.locals.RESIZABLE | pygame.locals.DOUBLEBUF, 16)
        
        self.x_scale_rate = new_width / 1600
        self.y_scale_rate = new_height / 900
        self.x_scale_diff = new_width/self.width
        self.y_scale_diff = new_height/self.height

        self.width, self.height = new_width, new_height

        for scale_object in self.objects_to_scale:
            scale_object.scale_parameters(self.x_scale_rate, self.y_scale_rate)

        for scale_object in self.text_alerts:
            scale_object.scale_parameters(self.x_scale_rate, self.y_scale_rate)

        scaled_group_path = pygame.sprite.Group()
        for scale_object in self.path_collisions:
            # Calculate new positions 
            new_width = scale_object.rect.width * self.x_scale_diff
            new_height = scale_object.rect.height * self.y_scale_diff
            new_x = scale_object.rect.x * self.x_scale_diff
            new_y = scale_object.rect.y * self.y_scale_diff
            
            scaled_sprite = pygame.sprite.Sprite()
            scaled_sprite.rect = pygame.Rect(new_x, new_y, new_width, new_height)
            scaled_group_path.add(scaled_sprite)

        self.path_collisions = scaled_group_path
       
        scaled_group_other = pygame.sprite.Group()
        for scale_object in self.other_obstacles_collisions:
            # Calculate new positions 
            new_width = scale_object.rect.width * self.x_scale_diff
            new_height = scale_object.rect.height * self.y_scale_diff
            new_x = scale_object.rect.x * self.x_scale_diff
            new_y = scale_object.rect.y * self.y_scale_diff
            
            scaled_sprite = pygame.sprite.Sprite()
            scaled_sprite.rect = pygame.Rect(new_x, new_y, new_width, new_height)
            scaled_group_other.add(scaled_sprite)

        self.other_obstacles_collisions = scaled_group_other

        for scale_object in self.enemies:
            scale_object.scale_parameters(self.x_scale_rate, self.y_scale_rate, self.x_scale_diff, self.y_scale_diff)

        for scale_object in self.towers:
            scale_object.scale_parameters(self.x_scale_rate, self.y_scale_rate)

    def run(self):
        """
        Main game loop that handles all game events, updates, and rendering.

        The function manages two main states:
        - If `self.show_main_menu` is True, it displays the main menu and handles menu interactions.
        - Otherwise, it updates the game world, including towers, enemies, and UI elements, and handles player actions.

        During the game loop, the function continuously checks for user input, such as mouse clicks and key presses,
        and updates the game state accordingly. It also scales the game window when resized, handles tower placement,
        upgrades, and removal, and manages game pause/play functionality. The loop continues running until the player
        chooses to exit the game.

        Returns:
            None
        """
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
                                        ResourceManager.set_sounds_volume(0)
                                    else:
                                        self.sound_play = True
                                        ResourceManager.set_sounds_volume(0.015)
                                case "new_game":
                                    self.handle_restart_game()
                                    selected_tower = None
                                    drag_object_name = None
                                case "countinue":
                                    self.show_main_menu = False
                                case "back_to_menu":
                                    self.end_game = False
                                    self.game_running = False
                                    self.player_won = None
                                    selected_tower = None
                                    drag_object_name = None
                                case "exit_game":
                                    running = False
                                case _:
                                    pass 
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and self.game_running:
                            self.show_main_menu = False

                    elif event.type == pygame.VIDEORESIZE:
                        self.scale_game(event.w,  event.h)
                        self.drag_object = None   
                        selected_tower = None

            else:                
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
                                    
                                    # Buying a tower
                                    buy_value = selected_tower.upgrade_tower(clicked_position, self.money, self.text_alerts)
                                    
                                    if buy_value >= 0:
                                        
                                        self.money -= buy_value
                                            
                                    # Selling a tower
                                    sell_value = selected_tower.sell_tower(clicked_position)
                                       
                                    if sell_value >= 0:
                                        
                                        self.money += sell_value
                                        self.towers.remove(selected_tower)
                                        
                                    # Interacting with tower menu
                                    target_mode_arrow_clicked = selected_tower.change_tower_target_mode(clicked_position)
                                    menu_page_arrow_clicked = selected_tower.tower_menu.manage_tower_menu_page(clicked_position)
                                    
                                    
                                    if buy_value < 0 and sell_value < 0 and not target_mode_arrow_clicked and not menu_page_arrow_clicked:
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
                                                self.time_scale = 1
                                                self.fps = 60
                                                self.sped_up = False
                                            else:
                                                self.time_scale = 2
                                                self.fps = 120
                                                self.sped_up = True

                                        elif drag_object_name == "music":
                                            if self.sound_play:
                                                self.sound_play = False
                                                ResourceManager.set_sounds_volume(0)
                                            else:
                                                self.sound_play = True
                                                ResourceManager.set_sounds_volume(0.015)

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
                                        self.text_alerts.add(TextAlert("Not enough money!", 1000, (255, 0, 0), self.x_scale_rate, self.y_scale_rate))
                                        continue
                                    
                                    match drag_object_name:
                                        case "archer_tower":
                                            tower = ArcherTower(clicked_position[0]-3 * self.y_scale_rate, clicked_position[1]-42 * self.y_scale_rate, self.x_scale_rate, self.y_scale_rate)

                                        case "magic_tower":
                                            tower = MagicTower(clicked_position[0]-3 * self.y_scale_rate, clicked_position[1]-42 * self.y_scale_rate, self.x_scale_rate, self.y_scale_rate)
                                            
                                        case "cannon_tower":
                                            tower = CannonTower(clicked_position[0]-3 * self.x_scale_rate, clicked_position[1]-42 * self.y_scale_rate, self.x_scale_rate, self.y_scale_rate)
                                            
                                    self.money -= new_tower_cost
                                    self.building_sound.play()
                                    self.towers.add(tower)
                                    self.drag_object = None
                                    
                                else:
                                    
                                    self.text_alerts.add(TextAlert("Can't place a tower here!", 2000, (255, 0, 0), self.x_scale_rate, self.y_scale_rate))


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

                    elif event.type == pygame.VIDEORESIZE:
                        self.scale_game(event.w,  event.h)      
                        self.drag_object = None
                        selected_tower = None                  

            pygame.display.flip()
   
            self.fpsClock.tick(self.fps)
            self.delta_time = self.fpsClock.get_time() * self.time_scale
