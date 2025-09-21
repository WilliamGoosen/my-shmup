import pygame as pg
from states.base_state import BaseState
from utilities import draw_text, draw_lives, draw_health_bar, draw_icon, draw_icon_text, draw_confirm_popup
from settings import *

class PauseState(BaseState):
    """State for handling game pause functionality."""
    def __init__(self, game):
        super().__init__(game)        
        self.show_confirmation = False
        self.pending_action = None        

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

    def draw(self, surface):
        """Render pause state to surface."""
        self.game.all_sprites_group.draw(surface)
        overlay = pg.Surface((self.game.WIDTH, self.game.HEIGHT), pg.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        surface.blit(overlay, (0, 0))

        draw_text(
             surface,
             "Score: " + str(self.game.score),
             22,
             self.game.WIDTH / 2,
             self.game.HEIGHT * 0.01,
             self.game.font_name,
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
             self.game.player.shield
        )
        
        self.draw_pause_menu(surface)
        if self.show_confirmation:
            draw_confirm_popup(surface, self.game)    

    def draw_pause_menu(self, surface):
        icon_x = self.game.WIDTH * 0.42
        icon_text_padding_x = 0.06
        text_x = icon_x + self.game.WIDTH * icon_text_padding_x
        icon_y = self.game.HEIGHT * 0.7
        icon_text_padding_y = 0.026
        text_y = icon_y + self.game.WIDTH * icon_text_padding_y

        draw_text(surface, "PAUSED", 48, self.game.WIDTH / 2, self.game.HEIGHT / 4, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
        draw_icon_text(surface, "Resume", 22, text_x, text_y, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], self.game.WIDTH * 0.07, self.game.HEIGHT * 0.92)
        draw_icon_text(surface, "Quit to Title", 18, self.game.WIDTH * 0.11, self.game.HEIGHT * 0.940, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["enter_icon"], self.game.WIDTH * 0.92, self.game.HEIGHT * 0.915)
        draw_icon_text(surface, "Settings", 18, self.game.WIDTH * 0.78, self.game.HEIGHT * 0.940, self.game.font_name)