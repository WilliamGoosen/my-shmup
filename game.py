import pygame as pg
from settings import BG_COLOUR
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from systems import GraphicsManager, SoundManager
    from states.base_state import BaseState
    from player import Player


class Game:
    """A container to hold all game components and the current state."""
    def __init__(self):
        # Managers
        self.graphics_manager: GraphicsManager
        self.sound_manager: SoundManager

        # Sprite Groups
        self.all_sprites_group: pg.sprite.Group
        self.bullets_group: pg.sprite.Group
        self.stars_group: pg.sprite.Group 
        self.meteors_group: pg.sprite.Group
        self.powerups_group: pg.sprite.Group | None = None
        self.players_group: pg.sprite.Group
        self.bosses_group: pg.sprite.Group
        self.bullets_group: pg.sprite.Group
        # Screen Properties
        self.scale_factor: float = 1.0
        self.screen_width: int = 0
        self.screen_height: int = 0
        self.background_colour: tuple = BG_COLOUR # Use a simple default

        # State
        self.current_state: BaseState | None = None
        self.previous_state: str | None = None

        # Other important variables from main.py
        self.player: Player
        self.score: int = 0
        self.high_score: int = 0
        self.new_high_score_achieved: bool = False
        self.font_name: str = "arial"