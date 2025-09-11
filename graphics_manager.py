import pygame as pg
from os import path
from settings import *

class GraphicsManager:
    """A class to manage the loading and storage of graphics assets."""
    def __init__(self, ui_scale_factor):
        self.ui_scale_factor = ui_scale_factor
        self.meteoroid_images = self.load_meteoroid_images(ALL_METEOROID_FILES)
        self.meteoroid_images_medium = self.load_meteoroid_images(MEDIUM_METEOROID_FILES)
        self.icons = {}
        self.arrows = {}
        self.arrows_list = []
        self.highlight_index = 0
        self.last_highlight_time = 0
        self.highlight_delay = 600
        self.base_height = BASE_HEIGHT
        self.base_width = BASE_WIDTH
        self.background_image = None
        self.load_background()


    def load_meteoroid_images(self, meteoroid_filenames):
        """Loads and returns a list of meteoroid image surfaces."""
        meteor_images = []
        for img in meteoroid_filenames:
            img_surface = pg.image.load(path.join("img", img)).convert_alpha()
            img_surface.set_colorkey(BLACK)
            meteor_images.append(img_surface)
        return meteor_images
    
    # --- NEW INTERNAL HELPER METHOD ---
    def _load_image_base(self, filename, default_scale, special_scales={}, scale_factor=1.0):
        """Helper method to load, scale, and return an image and its key."""
        key = path.splitext(filename)[0]  # Get the key from the filename
        image = pg.image.load(path.join("img", filename)).convert_alpha()
        # Apply special scale if it exists, otherwise use the default
        scale = special_scales.get(key, default_scale) * scale_factor
        scaled_image = pg.transform.scale_by(image, scale)
        return key, scaled_image
    # --- END HELPER METHOD ---

    def load_icons(self):
        self.icons = {}
        icon_list = ICON_LIST # Your full icon list
        special_scales = {"enter_icon": 4/3} # Define special cases

        for file in icon_list:
            key, loaded_icon = self._load_image_base(file, default_scale=2, special_scales=special_scales, scale_factor=self.ui_scale_factor)
            self.icons[key] = loaded_icon

    def load_arrows(self):
        self.arrows = {}
        icon_list = ARROW_LIST # Your arrow list

        for file in icon_list:
            key, loaded_arrow = self._load_image_base(file, default_scale=1.5, scale_factor=self.ui_scale_factor)
            loaded_arrow.set_alpha(150)  # Special processing for arrows
            self.arrows[key] = loaded_arrow

        self.arrows_list = [self.arrows["up_icon"], self.arrows["down_icon"], self.arrows["left_icon"], self.arrows["right_icon"]]
        
        
    def load_background(self):
        background_image_original = pg.image.load(path.join("img", "starfield_576x720.png")).convert_alpha()
        self.background_image = pg.transform.smoothscale_by(background_image_original, self.ui_scale_factor)