import pygame as pg
from states.base_state import BaseState
from states import PauseState, TitleState
from utilities import draw_text, draw_icon, draw_icon_text, draw_confirm_popup, reset_high_score
from settings import *

class SettingsState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.current_volume_step = int(self.game.sound_manager.music_volume * 10)
        self.current_sound_volume_step = int(self.game.sound_manager.sound_volume * 10)
        self.show_confirmation = False
        self.pending_action = False
        self.high_score_reset_message = False
        self.now = pg.time.get_ticks()
        self.message_timer = pg.time.get_ticks()
        
    def startup(self):
        super().startup()
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.show_confirmation:
                if event.key == pg.K_y:
                    if self.pending_action == "reset_high_score":
                        reset_high_score(self.game)
                        self.high_score_reset_message = True
                        self.message_timer = pg.time.get_ticks()
                    self.show_confirmation = False
                    self.pending_action = None
                elif event.key == pg.K_n or event.key == pg.K_ESCAPE:
                    self.show_confirmation = False
                    self.pending_action = None

            else:                                   
                if event.key == pg.K_RIGHT and self.current_volume_step < 10:
                    self.current_volume_step += 1
                    new_volume = self.current_volume_step / 10
                    self.game.sound_manager.set_music_volume(new_volume)
                if event.key == pg.K_LEFT and self.current_volume_step > 0:
                    self.current_volume_step -= 1
                    new_volume = self.current_volume_step / 10
                    self.game.sound_manager.set_music_volume(new_volume)
                if event.key == pg.K_UP and self.current_sound_volume_step < 10:
                    self.current_sound_volume_step += 1
                    new_sound_volume = self.current_sound_volume_step / 10
                    self.game.sound_manager.set_sound_volume(new_sound_volume)
                if event.key == pg.K_DOWN and self.current_sound_volume_step > 0:
                    self.current_sound_volume_step -= 1
                    new_sound_volume = self.current_sound_volume_step / 10
                    self.game.sound_manager.set_sound_volume(new_sound_volume)
                if event.key == pg.K_ESCAPE:
                    self.return_state = self.game.previous_state                    
                    if self.return_state == "PAUSE":
                        self.done = True
                        self.next_state = "PAUSE"
                        self.return_state = "RESUME"                       
                    elif self.return_state == "TITLE":
                        self.done = True
                        self.next_state = "TITLE"
                        self.return_state = "RESUME_GAME"                        
                if event.key == pg.K_s:
                    self.game.sound_manager.sound_enabled = not self.game.sound_manager.sound_enabled
                    self.game.sound_manager.set_sound_volume(1.0 if self.game.sound_manager.sound_enabled else 0.0)
                if event.key == pg.K_m:
                    self.game.sound_manager.music_enabled = self.game.sound_manager.toggle_music()
                if event.key == pg.K_r:
                    self.pending_action = "reset_high_score"
                    self.show_confirmation = True
                self.now = pg.time.get_ticks()
                if self.now - self.game.graphics_manager.last_highlight_time > self.game.graphics_manager.highlight_delay:
                    self.game.graphics_manager.last_highlight_time = self.now
                    for icon in self.game.graphics_manager.arrows_list:
                        icon.set_alpha(150)
                    self.game.graphics_manager.arrows_list[self.game.graphics_manager.highlight_index].set_alpha(255)
                    self.game.graphics_manager.highlight_index = (self.game.graphics_manager.highlight_index + 1) % 4
                # Check if the message timer has expired
                if self.high_score_reset_message:
                    self.now = pg.time.get_ticks()
                    if self.now - self.message_timer > MESSAGE_DISPLAY_TIME:
                        self.high_score_reset_message = False  # Hide the message       
    
    def update(self, dt):
        return super().update(dt)
    
    def draw(self, surface):
        surface.blit(self.game.graphics_manager.background_image, (0, 0))
        self.draw_settings_menu(surface)
        if self.show_confirmation:
            draw_confirm_popup(surface, self.game)
    
    def draw_settings_menu(self, surface):
        icon_x = self.game.WIDTH * 0.37
        icon_text_padding_x = 0.05
        text_x = icon_x + self.game.WIDTH * icon_text_padding_x
        icon_y = self.game.HEIGHT * 2 / 5
        icon_text_padding_y = 0.026
        text_y = icon_y + self.game.WIDTH * icon_text_padding_y
        y_increment = 40

        draw_text(surface, "High Score: " + str(self.game.high_score), 22, self.game.WIDTH * 0.5, self.game.HEIGHT * 0.02, self.game.font_name) 
        draw_text(surface, "SETTINGS", 48, self.game.WIDTH * 0.5, self.game.HEIGHT * 0.25, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["s_icon"], icon_x, icon_y + icon_text_padding_y)
        draw_icon_text(surface, f"Sound: {"ON" if self.game.sound_manager.sound_enabled else "OFF"}", 22, text_x, text_y, self.game.font_name) 

        draw_icon(surface, self.game.graphics_manager.icons["m_icon"], icon_x, icon_y + icon_text_padding_y + y_increment)
        draw_icon_text(surface, f"Music: {"ON" if self.game.sound_manager.music_enabled else "OFF"}", 22, text_x, text_y + y_increment, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["r_icon"], icon_x, icon_y + icon_text_padding_y + 2 * y_increment)
        draw_icon_text(surface, "Reset High Score", 22, text_x, text_y + 2 * y_increment, self.game.font_name)
        if self.high_score_reset_message:
            draw_text(surface, "High Score Reset!", 22, self.game.WIDTH / 2, self.game.HEIGHT * 0.56, self.game.font_name, GREEN)

        draw_text(surface, f"Music Volume: {self.current_volume_step}", 22, self.game.WIDTH // 2, self.game.HEIGHT * 3 / 5, self.game.font_name)
        draw_text(surface, f"Sound Volume: {self.current_sound_volume_step}", 22, self.game.WIDTH // 2, self.game.HEIGHT * 3.6 / 5, self.game.font_name)

        block_width = int(15 / 576 * self.game.WIDTH)
        block_height = 15 / 720 * self.game.HEIGHT
        block_spacing = 0
        icon_spacing = 5 / 576 * self.game.WIDTH
        start_x = self.game.WIDTH // 2 - (10 * (block_width + block_spacing)) // 2  # Center the row
        last_block_x = start_x + (11 * (block_width + block_spacing)) - 1.5 * block_spacing
        plus_x = last_block_x + 1.6 * icon_spacing
        minus_x = start_x - (block_width + icon_spacing)

        for i in range(1, 11):
            if i <= self.current_volume_step:
                color = GREEN  # Filled block for active volume
            else:
                color = GRAY   # Empty block for inactive
            # Draw a rectangle for each block
            block_rect = pg.Rect(start_x, self.game.HEIGHT * 3.25 / 5, block_width, block_height)
            pg.draw.rect(surface, color, block_rect)
            start_x += block_width + block_spacing

        start_x = self.game.WIDTH // 2 - (10 * (block_width + block_spacing)) // 2  # Center the row
        last_sound_block_x = start_x + (11 * (block_width + block_spacing)) - 1.5 * block_spacing
        up_x = last_sound_block_x + 1.6 * icon_spacing
        down_x = start_x - (block_width + icon_spacing)

        for i in range(1, 11):
            if i <= self.current_sound_volume_step:
                color = GREEN  # Filled block for active volume
            else:
                color = GRAY   # Empty block for inactive
            # Draw a rectangle for each block
            block_rect = pg.Rect(start_x, self.game.HEIGHT * 3.85 / 5, block_width, block_height)
            pg.draw.rect(surface, color, block_rect)
            start_x += block_width + block_spacing


        draw_icon(surface, self.game.graphics_manager.icons["left_icon"], minus_x, self.game.HEIGHT * 3.2 / 5)
        draw_icon(surface, self.game.graphics_manager.icons["right_icon"], plus_x, self.game.HEIGHT * 3.2 / 5)

        draw_icon(surface, self.game.graphics_manager.icons["down_icon"], down_x, self.game.HEIGHT * 3.8 / 5)
        draw_icon(surface, self.game.graphics_manager.icons["up_icon"], up_x, self.game.HEIGHT * 3.8 / 5)

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], self.game.WIDTH * 0.07, self.game.HEIGHT * 0.92)
        draw_icon_text(surface, "Back", 18, self.game.WIDTH * 0.11, self.game.HEIGHT * 0.940, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], self.game.WIDTH * 0.92, self.game.HEIGHT * 0.92)
        draw_icon_text(surface, "Shoot", 18, self.game.WIDTH * 0.78, self.game.HEIGHT * 0.940, self.game.font_name)

        arrow_x = self.game.WIDTH * 0.945
        arrow_y = self.game.HEIGHT * 0.90
        draw_icon(surface, self.game.graphics_manager.arrows["right_icon"], arrow_x, arrow_y - 16)
        draw_icon(surface, self.game.graphics_manager.arrows["left_icon"], arrow_x - 2 * 16, arrow_y - 16)
        draw_icon(surface, self.game.graphics_manager.arrows["up_icon"], arrow_x - 16, arrow_y - 2 * 16)
        draw_icon(surface, self.game.graphics_manager.arrows["down_icon"], arrow_x - 16, arrow_y - 16)
        draw_icon_text(surface, "Move", 18, self.game.WIDTH * 0.78, self.game.HEIGHT * 0.89, self.game.font_name)