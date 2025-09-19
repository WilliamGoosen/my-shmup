import pygame as pg
from states.base_state import BaseState
from utilities import draw_text, draw_icon_text, draw_icon, draw_confirm_popup
from settings import *

class GameOverState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.show_confirmation = False
        self.pending_action = None
    
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
                    # start_game()
                    self.done = True
                    self.next_state = "PLAY"
                        # game.current_state = PlayState(game)
                        # game.current_state.startup()
                elif event.key == pg.K_q:
                    self.pending_action = "quit_game"
                    self.show_confirmation = True

                elif event.key == pg.K_ESCAPE:
                    self.done = True
                    self.next_state = "TITLE"
                        # game.current_state = TitleState(game)
                        # game.current_state.startup()
    
    def update(self, dt):
        # return super().update(dt)
        self.game.all_sprites_group.update(dt)
    
    def draw(self, surface):
        surface.blit(self.game.graphics_manager.background_image, (0, 0))
        self.draw_game_over_title(surface)
        if self.show_confirmation:
            draw_confirm_popup(surface, self.game)
    
    def draw_game_over_title(self, surface):
        icon_x = self.game.WIDTH * 0.42
        icon_text_padding_x = 0.06
        text_x = icon_x + self.game.WIDTH * icon_text_padding_x
        icon_y = self.game.HEIGHT * 0.7
        icon_text_padding_y = 0.026
        text_y = icon_y + self.game.WIDTH * icon_text_padding_y
        y_increment = 40

        draw_text(surface, "High Score: " + str(self.game.high_score), 22, self.game.WIDTH / 2, 15, self.game.font_name)
        draw_text(surface, "GAME OVER", 48, self.game.WIDTH / 2, self.game.HEIGHT / 4, self.game.font_name)
        draw_text(surface, "Score: " + str(self.game.score), 30, self.game.WIDTH / 2, self.game.HEIGHT * 2 / 5 + y_increment, self.game.font_name)

        if self.game.new_high_score_achieved:
            draw_text(surface, "NEW HIGH SCORE!", 30, self.game.WIDTH / 2, self.game.HEIGHT * 2 / 5, self.game.font_name, GREEN)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
        draw_icon_text(surface, "Try Again", 22, text_x, text_y, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], self.game.WIDTH * 0.07, self.game.HEIGHT * 0.92)
        draw_icon_text(surface, "Quit to Title", 18, self.game.WIDTH * 0.11, self.game.HEIGHT * 0.940, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["q_icon"], self.game.WIDTH * 0.93, self.game.HEIGHT * 0.92)
        draw_icon_text(surface, "Quit Game", 18, self.game.WIDTH * 0.770, self.game.HEIGHT * 0.940, self.game.font_name)

