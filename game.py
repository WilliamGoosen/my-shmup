import pygame as pg
from utilities import load_or_create_file
from settings import BG_COLOUR, HS_FILE, FONT_NAME
from systems import GraphicsManager, SoundManager
from states import TitleState
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from states.base_state import BaseState
    from player import Player


class Game:
    """A container to hold all game components and the current state."""
    def __init__(self, config: dict,scale_factor: float, screen_width: int, screen_height: int):
        self.config = config
        self.scale_factor = scale_factor
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.background_colour: tuple = BG_COLOUR
        self.music_volume = float(self.config.get("music_volume", 0.5))
        self.sound_volume = float(self.config.get("sound_volume", 0.5))
        
        # Managers
        self.graphics_manager: GraphicsManager = GraphicsManager(self.scale_factor)
        self.sound_manager: SoundManager = SoundManager(
            music_volume = self.music_volume,
            sound_volume = self.sound_volume
            )

        # Sprite Groups
        self.all_sprites_group: pg.sprite.Group = pg.sprite.Group()
        self.bullets_group: pg.sprite.Group = pg.sprite.Group()
        self.stars_group: pg.sprite.Group = pg.sprite.Group()
        self.meteors_group: pg.sprite.Group = pg.sprite.Group()
        self.powerups_group: pg.sprite.Group = pg.sprite.Group()
        self.players_group: pg.sprite.Group = pg.sprite.Group()
        self.bullets_group: pg.sprite.Group = pg.sprite.Group()
        self.bosses_group: pg.sprite.Group = pg.sprite.Group()
        self.boss_bullets_group: pg.sprite.Group = pg.sprite.Group()

        # State
        self.current_state: BaseState = TitleState(self)
        self.previous_state: str | None = None

        # Other important variables from main.py
        self.player: Player
        self.boss_defeated: bool = False
        self.score: int = 0
        self.high_score: int = int(load_or_create_file(HS_FILE, 0))
        self.new_high_score_achieved: bool = False
        self.font_name: str = pg.font.match_font(FONT_NAME)