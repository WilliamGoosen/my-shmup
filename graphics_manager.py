import pygame as pg
from os import path
from settings import *

class GraphicsManager:
    """A class to manage the loading and storage of graphics assets."""
    def __init__(self):
        self.meteoroid_images = []


    def load_meteoroid_images(self, meteoroid_filenames):
        """Loads and returns a list of meteoroid image surfaces."""
        self.meteor_images = []
        for img in meteoroid_filenames:
            img_surface = pg.image.load(path.join("img", img)).convert_alpha()
            img_surface.set_colorkey(BLACK)
            self.meteor_images.append(img_surface)
        return self.meteor_images