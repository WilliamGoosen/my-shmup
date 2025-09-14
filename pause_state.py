import pygame as pg
from base_state import BaseState

class PauseState(BaseState):
    """State for handling game pause functionality."""

    def __init__(self, game):
        super().__init__(game)
        print("PauseState initialized")

    def startup(self):
        """Initialize pause state resources."""
        super().startup()

    def get_event(self, event):
        """Handle input events for pause state."""
        if event.type == pg.KEYDOWN:
            print(f"PauseState received key: {event.key}")

    def update(self, dt):
        """Update pause state logic."""
        pass

    def draw(self, surface):
        """Render pause state to surface."""
        pass