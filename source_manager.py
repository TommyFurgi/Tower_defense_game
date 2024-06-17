import pygame
import os
import json
from PIL import Image

class SourceManager():
    """
    A class to manage loading and accessing game assets such as images, sounds,
    rectangles, and paths.
    """
    _images = {}
    _sounds = {}
    _rectangles = {}
    _paths = {}

    @classmethod
    def load_all(cls, images_folder, sounds_folder, environment_folder, paths_file):
        """
        Load all game assets including images, sounds, rectangles, and paths.

        Args:
            images_folder (str): The folder path containing image assets.
            sounds_folder (str): The folder path containing sound assets.
            environment_folder (str): The folder path containing environment assets.
            paths_file (str): The name of the JSON file containing paths data.
        """
        cls.load_images(images_folder)
        cls.load_sounds(sounds_folder)
        cls.load_rectangles(environment_folder)
        cls.load_paths(environment_folder, paths_file)

    @classmethod
    def load_images(cls, assets_folder):
        """
        Load images from the specified folder into the class.

        Args:
            assets_folder (str): The folder path containing image assets.
        """
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
        """
        Get the image object corresponding to the given name.

        Args:
            name (str): The name of the image asset to retrieve.

        Returns:
            pygame.Surface or PIL.Image.Image: The image object.
        """
        if name in cls._images:
            return cls._images[name]
        else:
            print(f"Image '{name}' not found.")
            return None

    @classmethod
    def load_sounds(cls, sounds_folder):
        """
        Load sounds from the specified folder into the class.

        Args:
            sounds_folder (str): The folder path containing sound assets.
        """
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
        """
        Get the sound object corresponding to the given name.

        Args:
            name (str): The name of the sound asset to retrieve.

        Returns:
            pygame.mixer.Sound: The sound object.
        """
        if name in cls._sounds:
            return cls._sounds[name]
        else:
            print(f"Sound '{name}' not found.")
            return None

    @classmethod
    def set_sounds_volume(cls, volume):
        """
        Set the volume for all loaded sounds.

        Args:
            volume (float): The volume level between 0.0 and 1.0.
        """
        if not 0.0 <= volume <= 1.0:
            print("Volume must be between 0.0 and 1.0")
            return
        
        for sound in cls._sounds.values():
            sound.set_volume(volume)

    @classmethod
    def load_rectangles(cls, rectangles_folder):
        """
        Load rectangles from text files in the specified folder into the class.

        Args:
            rectangles_folder (str): The folder path containing rectangle definition files.
        """
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
        """
        Get the list of rectangles corresponding to the given name.

        Args:
            name (str): The name associated with the rectangles.

        Returns:
            list: A list of tuples representing rectangles (x, y, width, height).
        """
        if name in cls._rectangles:
            return cls._rectangles[name]
        else:
            print(f"Rectangles for '{name}' not found.")
            return None

    @classmethod
    def load_paths(cls, root_folder, paths_file):
        """
        Load paths from a JSON file into the class.

        Args:
            root_folder (str): The root folder path containing the JSON file.
            paths_file (str): The name of the JSON file containing paths data.
        """
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
        """
        Get the path data corresponding to the given name.

        Args:
            name (str, optional): The name of the path. Defaults to 'default'.

        Returns:
            dict or None: The path data as a dictionary, or None if not found.
        """
        if name in cls._paths:
            return cls._paths.get(name)
        else:
            print(f"Path '{name}' not found.")
            return None
