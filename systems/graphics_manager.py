import pygame as pg
from pathlib import Path
from settings import *

class GraphicsManager:
    """A class to manage the loading and storage of graphics assets."""
    def __init__(self, ui_scale_factor):
        self.ui_scale_factor = ui_scale_factor
        self.meteoroid_images = self._load_meteoroid_images(ALL_METEOROID_FILES)
        self.meteoroid_images_medium = self._load_meteoroid_images(MEDIUM_METEOROID_FILES)
        self.player_image, self.player_icon = self._load_player_images()
        self.boss_image = self._load_boss_image()
        self.bullet_image, self.boss_bullet_image = self._load_bullet_images()
        self.icons = self._load_icons()
        self.arrows = self._load_arrows_dict()
        self.arrows_list = self._create_arrows_list(self.arrows)
        self.powerup_icons = self._load_powerup_icons()
        self.explosion_animations = self._load_explosion_animations()
        self.highlight_index = 0
        self.last_highlight_time = 0
        self.highlight_delay = 600
        self.base_height = BASE_HEIGHT
        self.base_width = BASE_WIDTH
        self.background_image = self._load_background()
        self.confirm_overlay, self.popup_bg = self._create_ui_surfaces()


    def _load_player_images(self) -> tuple[pg.Surface, pg.Surface]:
        player_image_original = pg.image.load(Path("img") / "playerShip1_orange.png").convert_alpha()
        player_image = pg.transform.scale_by(player_image_original, 0.5 * self.ui_scale_factor)
        player_icon = pg.transform.scale_by(player_image_original, 0.25 * self.ui_scale_factor)

        return player_image, player_icon
        
    def _load_boss_image(self) -> pg.Surface:
        boss_image_original = pg.image.load(Path("img") / "ufoRed.png").convert_alpha()
        boss_image = pg.transform.scale_by(boss_image_original, 3 * self.ui_scale_factor)
        return boss_image

    def _load_bullet_images(self) -> tuple[pg.Surface, pg.Surface]:
        bullet_image_original = pg.image.load(Path("img") / "laserRed16.png").convert_alpha()
        bullet_image = pg.transform.scale_by(bullet_image_original, self.ui_scale_factor)
        boss_bullet_image = pg.transform.rotate(bullet_image, 180)
        return bullet_image, boss_bullet_image


    def _load_meteoroid_images(self, meteoroid_filenames) -> list[pg.Surface]:
        """Loads and returns a list of meteoroid image surfaces."""
        meteor_images = []
        for img in meteoroid_filenames:
            img_surface = pg.image.load(Path("img") / img).convert_alpha()
            img_surface_scaled = pg.transform.scale_by(img_surface, self.ui_scale_factor)
            meteor_images.append(img_surface_scaled)
        return meteor_images
        
    # --- INTERNAL HELPER METHOD ---
    def _load_image_base(self, filename, default_scale, special_scales={}, scale_factor=1.0) -> tuple[str, pg.Surface]:
        """Helper method to load, scale, and return an image and its key."""
        key = Path(filename).stem  # Get the key from the filename
        image = pg.image.load(Path("img") / filename).convert_alpha()
        # Apply special scale if it exists, otherwise use the default
        scale = special_scales.get(key, default_scale) * scale_factor
        scaled_image = pg.transform.scale_by(image, scale)
        return key, scaled_image

    def _load_icons(self) -> dict[str, pg.Surface]:
        icons = {}
        special_scales = {"enter_icon": 4/3} # Define special cases

        for file in ICON_LIST:
            key, loaded_icon = self._load_image_base(file, default_scale=2, special_scales=special_scales, scale_factor=self.ui_scale_factor)
            icons[key] = loaded_icon
        return icons

    def _load_arrows_dict(self) -> dict[str, pg.Surface]:
        """Load all arrow icons into a dictionary"""
        arrows = {}

        for file in ARROW_LIST:
            key, loaded_arrow = self._load_image_base(file, default_scale=1.5, scale_factor=self.ui_scale_factor)
            loaded_arrow.set_alpha(150)  # Special processing for arrows
            arrows[key] = loaded_arrow
        
        return arrows

    def _create_arrows_list(self, arrows_dict: dict[str, pg.Surface]) -> list[pg.Surface]:

        return [
            arrows_dict["up_icon"],
            arrows_dict["down_icon"],
            arrows_dict["left_icon"],
            arrows_dict["right_icon"]
            ]
        
    def _load_powerup_icons(self) -> dict[str, pg.Surface]:
        powerup_icons = {}
        icon_list = POWERUP_LIST # Your full icon list
        special_scales = {"health_up": 1/2}
        
        for file in icon_list:
            key, loaded_icon = self._load_image_base(file, default_scale=1, special_scales=special_scales, scale_factor=self.ui_scale_factor)
            powerup_icons[key] = loaded_icon

        return powerup_icons
        
    def _load_background(self) -> pg.Surface:
        background_image_original = pg.image.load(Path("img") / "starfield_576x720.png").convert_alpha()
        background_image = pg.transform.smoothscale_by(background_image_original, self.ui_scale_factor)

        return background_image
        
    def _create_ui_surfaces(self) -> tuple[pg.Surface, pg.Surface]:
        screen_width = self.base_width * self.ui_scale_factor
        screen_height = self.base_height * self.ui_scale_factor
        confirm_overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        confirm_overlay.fill(CONFIRM_OVERLAY)
        
        popup_width = self.base_width * 0.4 * self.ui_scale_factor
        popup_height = self.base_height * 0.2 * self.ui_scale_factor
        popup_bg = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
        popup_bg.fill(RED)

        return confirm_overlay, popup_bg
        
    def _load_explosion_variant(self, base_name, frame_count, target_scale) -> list[pg.Surface]:
        frame_list = []
        for i in range(frame_count):
            filename = f"{base_name}0{i}.png" if i < 10 else f"{base_name}{i}.png"
            img = pg.image.load(Path("img") / filename).convert_alpha()
            img.set_colorkey(BLACK)
            scaled_img = pg.transform.scale_by(img, target_scale * self.ui_scale_factor)
            frame_list.append(scaled_img)
        
        return frame_list
    
    def _load_explosion_animations(self) -> dict[str, list[pg.Surface]]:
        explosion_animations = {}
        explosion_animations['large_explosion'] = self._load_explosion_variant('regularExplosion', 9, 0.5)
        explosion_animations['small_explosion'] = self._load_explosion_variant('regularExplosion', 9, 1 / 3.2)
        explosion_animations['player_explosion'] = self._load_explosion_variant('sonicExplosion', 9, 1.0)
        explosion_animations['boss_explosion'] = self._load_explosion_variant('sonicExplosion', 9, 3.3)

        return explosion_animations