import pygame as pg
from states.base_state import BaseState
from utilities import draw_text, draw_lives, draw_health_bar, draw_icon, draw_icon_text, draw_confirm_popup
from settings import *
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game
    from player import Player

class PauseState(BaseState):
    """State for handling game pause functionality."""
    def __init__(self, game: 'Game'):
        super().__init__(game)        
        self.show_confirmation = False
        self.pending_action = None 
        self.game = game       

    def startup(self):
        """Initialize pause state resources."""
        super().startup()

    def get_event(self, event):
        """Handle input events for pause state."""
        if event.type == pg.KEYDOWN:
            if self.show_confirmation:

                if event.key == pg.K_y:
                    if self.pending_action == "quit_to_title":
                        self.done = True
                        self.next_state = "TITLE"
                    self.show_confirmation = False
                    self.pending_action = None
                elif event.key == pg.K_n or event.key == pg.K_ESCAPE:
                    self.show_confirmation = False
                    self.pending_action = None

            else:
                if event.key == pg.K_SPACE:
                    self.done = True
                    self.next_state = "PLAY"
                    self.return_state = "RESUME_GAME"
                elif event.key == pg.K_ESCAPE:
                    self.pending_action = "quit_to_title"
                    self.show_confirmation = True
                elif event.key == pg.K_RETURN:
                    self.done = True                    
                    self.next_state = "SETTINGS"
                    self.game.previous_state = "PAUSE"

    def draw(self, surface: pg.Surface):
        """Render pause state to surface."""
        self.game.all_sprites_group.draw(surface)
        scale_factor = self.game.scale_factor
        screen_width = self.game.screen_width
        screen_height = self.game.screen_height
        font_name = self.game.font_name
        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        surface.blit(overlay, (0, 0))

        draw_text(
             surface,
             "Score: " + str(self.game.score),
             round(22 * scale_factor),
             screen_width / 2,
             screen_height * 0.01,
             font_name,
             WHITE
        )
        draw_lives(
             surface,
             self.game,
             self.game.player.lives,
             self.game.graphics_manager.player_icon
        )
        draw_health_bar(
             surface,
             self.game,
             self.game.player.health
        )
        
        self.draw_pause_menu(surface)
        if self.show_confirmation:
            draw_confirm_popup(surface, self.game)    

    def draw_pause_menu(self, surface: pg.Surface):
        scale_factor = self.game.scale_factor
        screen_width = self.game.screen_width
        screen_height = self.game.screen_height
        font_name = self.game.font_name
        icon_x = screen_width * 0.42
        text_x = icon_x + screen_width * 0.06
        icon_y = screen_height * 0.7
        text_y = icon_y + screen_width * 0.026

        draw_text(surface, "PAUSED", round(48 * scale_factor), screen_width / 2, screen_height / 4, font_name)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], icon_x, icon_y)
        draw_icon_text(surface, "Resume", round(22 * scale_factor), text_x, text_y, font_name)

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], screen_width * 0.07, screen_height * 0.92)
        draw_icon_text(surface, "Quit to Title", round(18 * scale_factor), screen_width * 0.11, screen_height * 0.940, font_name)

        draw_icon(surface, self.game.graphics_manager.icons["enter_icon"], screen_width * 0.92, screen_height * 0.915)
        draw_icon_text(surface, "Settings", round(18 * scale_factor), screen_width * 0.78, screen_height * 0.940, font_name)