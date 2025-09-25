import pygame as pg
from states.base_state import BaseState
from utilities import draw_text, draw_icon_text, draw_icon, draw_confirm_popup
from settings import *
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game
    from systems import GraphicsManager

class GameOverState(BaseState):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.show_confirmation = False
        self.pending_action = None
        self.game: Game = game
    
    def startup(self):
        super().startup()
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.show_confirmation:
                if event.key == pg.K_y:
                    if self.pending_action == "quit_game":
                        self.quit = True
                        self.done = True
                    self.show_confirmation = False
                    self.pending_action = None
                
                elif event.key == pg.K_n or event.key == pg.K_ESCAPE:
                    self.show_confirmation = False
                    self.pending_action = None
                    
            else:
                if event.key == pg.K_SPACE:
                    self.done = True
                    self.next_state = "PLAY"                        
                elif event.key == pg.K_q:
                    self.pending_action = "quit_game"
                    self.show_confirmation = True

                elif event.key == pg.K_ESCAPE:
                    self.done = True
                    self.next_state = "TITLE"
    
    def draw(self, surface):
        surface.blit(self.game.graphics_manager.background_image, (0, 0))
        self.draw_game_over_title(surface)
        if self.show_confirmation:
            draw_confirm_popup(surface, self.game)
    
    def draw_game_over_title(self, surface):
        scale_factor = self.game.scale_factor
        screen_width = self.game.screen_width
        screen_height = self.game.screen_height
        icon_x = self.game.screen_width * 0.42
        text_x = icon_x + self.game.screen_width * 0.06
        icon_y = self.game.screen_height * 0.7
        text_y = icon_y + self.game.screen_width * 0.026
        y_increment = 40 * scale_factor

        draw_text(surface, "High Score: " + str(self.game.high_score), round(22 * scale_factor), screen_width * 0.5, screen_height * 0.02, self.game.font_name)
        draw_text(surface, "GAME OVER", round(48 * scale_factor), screen_width / 2, screen_height / 4, self.game.font_name)
        draw_text(surface, "Score: " + str(self.game.score), round(30 * scale_factor), screen_width / 2, screen_height * 2 / 5 + y_increment, self.game.font_name)

        if self.game.new_high_score_achieved:
            draw_text(surface, "NEW HIGH SCORE!", round(30 * scale_factor), screen_width / 2, screen_height * 2 / 5, self.game.font_name, GREEN)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], icon_x, icon_y)
        draw_icon_text(surface, "Try Again", round(22 * scale_factor), text_x, text_y, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], screen_width * 0.07, screen_height * 0.92)
        draw_icon_text(surface, "Quit to Title", round(18 * scale_factor), screen_width * 0.11, screen_height * 0.940, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["q_icon"], screen_width * 0.93, screen_height * 0.92)
        draw_icon_text(surface, "Quit Game", round(18 * scale_factor), screen_width * 0.770, screen_height * 0.940, self.game.font_name)

