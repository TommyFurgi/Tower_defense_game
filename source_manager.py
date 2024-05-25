import pygame
import os
from PIL import Image

class SourceManager():
    _images = {}
    _sounds = {}
    _rectangles = {}


    @classmethod
    def load_images(cls, assets_folder):
        for root, _, files in os.walk(assets_folder):
            for filename in files:
                if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(root, filename)
                    if name not in cls._images:
                        if 'enemies' in path:
                            cls._images[name] = Image.open(path)
                        else:
                            cls._images[name] = pygame.image.load(path)


    @classmethod
    def get_image(cls, name):
        return cls._images.get(name)
    

    @classmethod
    def load_sounds(cls, sounds_folder):
        for root, dirs, files in os.walk(sounds_folder):
            for filename in files:
                if filename.endswith(('.mp3', '.wav')):
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(root, filename)
                    if name not in cls._sounds:
                        cls._sounds[name] = pygame.mixer.Sound(path)


    @classmethod
    def get_sound(cls, name):
        return cls._sounds.get(name)
    

    @classmethod
    def set_sounds_volume(cls, volume):
        if not 0.0 <= volume <= 1.0:
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
                    except FileNotFoundError:
                        print(f"File '{filename}' not found. No rectangles loaded.")

                    cls._rectangles[name] = rectangles
        

    @classmethod
    def get_rectangles(cls, name):
        return cls._rectangles.get(name)