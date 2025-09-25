import pygame as pg
from states.base_state import BaseState
from utilities import draw_icon, draw_icon_text, draw_text
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game

class TitleState(BaseState):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.game = game

    def startup(self):
        super().startup()

    def get_event(self, event):
        """Handle imput events for title state"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                    self.done = True
                    self.next_state = "PLAY"
                    
            elif event.key == pg.K_RETURN:
                self.done = True
                self.next_state = "SETTINGS"
                self.game.previous_state = "TITLE"
            elif event.key == pg.K_ESCAPE:
                self.quit = True
                self.done = True
    
    def draw(self, surface):
        surface.blit(self.game.graphics_manager.background_image, (0, 0))
        self.draw_title_menu(surface)

    def draw_title_menu(self, surface):
        scale_factor = self.game.scale_factor
        screen_width = self.game.screen_width
        screen_height = self.game.screen_height
        icon_x = self.game.screen_width * 0.40
        text_x = icon_x + self.game.screen_width * 0.06
        icon_y = self.game.screen_height * 0.7
        text_y = icon_y + self.game.screen_width * 0.026

        draw_text(surface, "High Score: " + str(self.game.high_score), round(22 * scale_factor), screen_width * 0.5, screen_height * 0.02, self.game.font_name)
        draw_text(surface, "SHMUP!", round(64 * scale_factor), screen_width / 2, screen_height / 4, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], icon_x, icon_y)
        draw_icon_text(surface, "Start Game", round(22 * scale_factor), text_x, text_y, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["enter_icon"], screen_width * 0.92, screen_height * 0.915)
        draw_icon_text(surface, "Settings", round(18 * scale_factor), screen_width * 0.78, screen_height * 0.940, self.game.font_name) 

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], screen_width * 0.07, screen_height * 0.92)
        draw_icon_text(surface, "Quit Game", round(18 * scale_factor), screen_width * 0.11, screen_height * 0.940, self.game.font_name)