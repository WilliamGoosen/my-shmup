import pygame as pg
from settings import BG_COLOUR

class Game:
    """A container to hold all game components and the current state."""
    def __init__(self):
        # Managers
        self.graphics_manager = None
        self.sound_manager = None

        # Sprite Groups
        self.all_sprites_group = None
        self.bullets_group = None
        self.stars_group = None
        self.meteors_group = None
        self.powerups_group = None
        self.players_group = None

        # Screen Properties
        self.WIDTH = 0
        self.HEIGHT = 0
        self.BG_COLOUR = pg.Color(BG_COLOUR) # Use a simple default

        # State
        self.current_state = None

        # Other important variables from main.py
        self.score = 0
        self.high_score = 0
        self.font_name = None