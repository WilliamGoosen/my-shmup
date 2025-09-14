import pygame as pg
from base_state import BaseState
from utilities import draw_icon, draw_icon_text, draw_text

class TitleState(BaseState):
    def __init__(self, game):
        super().__init__(game)

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
                self.return_state = "TITLE"
            elif event.key == pg.K_ESCAPE:
                self.quit = True
                self.done = True

    def update(self, dt):
        self.game.all_sprites_group.update(dt)

    def draw(self, surface):
        surface.blit(self.game.graphics_manager.background_image, (0, 0))
        self.draw_title_menu(surface)

    def draw_title_menu(self, surface):
        icon_x = self.game.WIDTH * 0.40
        icon_text_padding_x = 0.06
        text_x = icon_x + self.game.WIDTH * icon_text_padding_x
        icon_y = self.game.HEIGHT * 0.7
        icon_text_padding_y = 0.026
        text_y = icon_y + self.game.WIDTH * icon_text_padding_y

        draw_text(surface, "High Score: " + str(self.game.high_score), 22, self.game.WIDTH * 0.5, self.game.HEIGHT * 0.02, self.game.font_name)
        draw_text(surface, "SHMUP!", 64, self.game.WIDTH / 2, self.game.HEIGHT / 4, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
        draw_icon_text(surface, "Start Game", 22, text_x, text_y, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["enter_icon"], self.game.WIDTH * 0.92, self.game.HEIGHT * 0.915)
        draw_icon_text(surface, "Settings", 18, self.game.WIDTH * 0.78, self.game.HEIGHT * 0.940, self.game.font_name) 

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], self.game.WIDTH * 0.07, self.game.HEIGHT * 0.92)
        draw_icon_text(surface, "Quit Game", 18, self.game.WIDTH * 0.11, self.game.HEIGHT * 0.940, self.game.font_name)