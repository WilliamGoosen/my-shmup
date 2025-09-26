import pygame as pg
from os import path
from settings import *

class GraphicsManager:
    """A class to manage the loading and storage of graphics assets."""
    def __init__(self, ui_scale_factor):
        self.ui_scale_factor = ui_scale_factor
        self.meteoroid_images = self.load_meteoroid_images(ALL_METEOROID_FILES)
        self.meteoroid_images_medium = self.load_meteoroid_images(MEDIUM_METEOROID_FILES)
        self.player_image: pg.Surface
        self.player_icon: pg.Surface
        self.bullet_image: pg.Surface
        self.icons = {}
        self.arrows = {}
        self.powerup_icons = {}
        self.arrows_list = []
        self.explosion_animations = {}
        self.highlight_index = 0
        self.last_highlight_time = 0
        self.highlight_delay = 600
        self.base_height = BASE_HEIGHT
        self.base_width = BASE_WIDTH
        self.background_image: pg.Surface
        self.confirm_overlay: pg.Surface
        self.popup_bg: pg.Surface
        self.create_ui_surfaces()
        self.load_background()
        self.load_player_image()
        self.load_bullet_image()
        self.load_icons()
        self.load_arrows()
        self.load_powerup_icons()
        self.load_explosion_animations()        


    def load_player_image(self):
        player_image_original = pg.image.load(path.join("img", "playerShip1_orange.png")).convert_alpha()
        self.player_image = pg.transform.scale_by(player_image_original, 0.5 * self.ui_scale_factor)
        self.player_icon = pg.transform.scale_by(player_image_original, 0.25 * self.ui_scale_factor)
        
    def load_bullet_image(self):
        bullet_image_original = pg.image.load(path.join("img", "laserRed16.png")).convert_alpha()
        self.bullet_image = pg.transform.scale_by(bullet_image_original, self.ui_scale_factor)
        

    def load_meteoroid_images(self, meteoroid_filenames):
        """Loads and returns a list of meteoroid image surfaces."""
        meteor_images = []
        for img in meteoroid_filenames:
            img_surface = pg.image.load(path.join("img", img)).convert_alpha()
            img_surface_scaled = pg.transform.scale_by(img_surface, self.ui_scale_factor)
            # img_surface.set_colorkey(BLACK)
            meteor_images.append(img_surface_scaled)
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
        
    def load_powerup_icons(self):
        self.powerup_icons = {}
        icon_list = POWERUP_LIST # Your full icon list
        special_scales = {"health_up": 1/2}
        
        for file in icon_list:
            key, loaded_icon = self._load_image_base(file, default_scale=1, special_scales=special_scales, scale_factor=self.ui_scale_factor)
            self.powerup_icons[key] = loaded_icon
        
    def load_background(self):
        background_image_original = pg.image.load(path.join("img", "starfield_576x720.png")).convert_alpha()
        self.background_image = pg.transform.smoothscale_by(background_image_original, self.ui_scale_factor)
        
        
    def create_ui_surfaces(self):
        screen_width = self.base_width * self.ui_scale_factor
        screen_height = self.base_height * self.ui_scale_factor
        self.confirm_overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        self.confirm_overlay.fill(CONFIRM_OVERLAY)
        
        popup_width = self.base_width * 0.4 * self.ui_scale_factor
        popup_height = self.base_height * 0.2 * self.ui_scale_factor
        self.popup_bg = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
        self.popup_bg.fill(RED)
        
    def _load_explosion_variant(self, base_name, frame_count, target_scale, target_key):
        frame_list = []
        for i in range(frame_count):
            filename = f"{base_name}0{i}.png" if i < 10 else f"{base_name}{i}.png"
            img = pg.image.load(path.join("img", filename)).convert_alpha()
            img.set_colorkey(BLACK)
            scaled_img = pg.transform.scale_by(img, target_scale * self.ui_scale_factor)
            frame_list.append(scaled_img)
        self.explosion_animations[target_key] = frame_list
    
    def load_explosion_animations(self):
        self.explosion_animations = {}
        self._load_explosion_variant('regularExplosion', 9, 0.5, 'large_explosion')
        self._load_explosion_variant('regularExplosion', 9, 1 / 3.2, 'small_explosion')
        self._load_explosion_variant('sonicExplosion', 9, 1.0, 'player_explosion')
        self._load_explosion_variant('sonicExplosion', 9, 3.3, 'boss_explosion')