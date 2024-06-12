import pygame
import os
import json
from PIL import Image

class SourceManager():
    _images = {}
    _sounds = {}
    _rectangles = {}
    _paths = {}

    @classmethod
    def load_all(cls, images_folder, sounds_folder, environment_folder, paths_file):
        cls.load_images(images_folder)
        cls.load_sounds(sounds_folder)
        cls.load_rectangles(environment_folder)
        cls.load_paths(environment_folder, paths_file)

    @classmethod
    def load_images(cls, assets_folder):
        for root, _, files in os.walk(assets_folder):
            for filename in files:
                if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(root, filename)
                    if name not in cls._images:
                        try:
                            if 'enemies' in path:
                                cls._images[name] = Image.open(path)
                            else:
                                cls._images[name] = pygame.image.load(path)
                        except Exception as e:
                            print(f"Error loading image '{filename}': {e}")

    @classmethod
    def get_image(cls, name):
        if name in cls._images:
            return cls._images[name]
        else:
            print(f"Image '{name}' not found.")
            return None

    @classmethod
    def load_sounds(cls, sounds_folder):
        for root, _, files in os.walk(sounds_folder):
            for filename in files:
                if filename.endswith(('.mp3', '.wav')):
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(root, filename)
                    if name not in cls._sounds:
                        try:
                            cls._sounds[name] = pygame.mixer.Sound(path)
                        except Exception as e:
                            print(f"Error loading sound '{filename}': {e}")

    @classmethod
    def get_sound(cls, name):
        if name in cls._sounds:
            return cls._sounds[name]
        else:
            print(f"Sound '{name}' not found.")
            return None

    @classmethod
    def set_sounds_volume(cls, volume):
        if not 0.0 <= volume <= 1.0:
            print("Volume must be between 0.0 and 1.0")
            return
        
        for sound in cls._sounds.values():
            sound.set_volume(volume)

    @classmethod
    def load_rectangles(cls, rectangles_folder):
        for filename in os.listdir(rectangles_folder):
            if filename.endswith('.txt'):
                name = os.path.splitext(filename)[0]
                path = os.path.join(rectangles_folder, filename)
                if name not in cls._rectangles:
                    rectangles = []  
                    try:
                        with open(path, "r") as file:  
                            for line in file:
                                rect_x, rect_y, rect_width, rect_height = map(int, line.strip().split())
                                rectangles.append((rect_x, rect_y, rect_width, rect_height))
                        cls._rectangles[name] = rectangles
                    except FileNotFoundError:
                        print(f"File '{filename}' not found. No rectangles loaded.")
                    except ValueError as e:
                        print(f"Error processing file '{filename}': {e}")

    @classmethod
    def get_rectangles(cls, name):
        if name in cls._rectangles:
            return cls._rectangles[name]
        else:
            print(f"Rectangles for '{name}' not found.")
            return None

    @classmethod
    def load_paths(cls, root_folder, paths_file):
        for root, _, files in os.walk(root_folder):
            if paths_file in files:
                file_path = os.path.join(root, paths_file)
                try:
                    with open(file_path, "r") as file:
                        cls._paths = json.load(file)
                        break  # Stop searching after the file is found
                except FileNotFoundError:
                    print(f"File '{paths_file}' not found. No paths loaded.")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file '{paths_file}'.")

    @classmethod
    def get_path(cls, name='default'):
        if name in cls._paths:
            return cls._paths.get(name)
        else:
            print(f"Path '{name}' not found.")
            return None
