import pygame as pg
from states.base_state import BaseState
from utilities import draw_text, draw_icon, draw_icon_text, draw_confirm_popup, reset_high_score, update_config
from settings import *
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game

class SettingsState(BaseState):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.current_volume_step = int(self.game.sound_manager.music_volume * 10)
        self.current_sound_volume_step = int(self.game.sound_manager.sound_volume * 10)
        self.show_confirmation = False
        self.pending_action = False
        self.high_score_reset_message = False
        self.animation_frame_time = 0
        self.message_timer = 0
        self.game = game
        
    def startup(self):
        super().startup()
    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.show_confirmation:
                if event.key == pg.K_y:
                    if self.pending_action == "reset_high_score":
                        reset_high_score(self.game)
                        self.high_score_reset_message = True
                        self.message_timer = 0
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
                    update_config("music_volume", new_volume)

                if event.key == pg.K_LEFT and self.current_volume_step > 0:
                    self.current_volume_step -= 1
                    new_volume = self.current_volume_step / 10
                    self.game.sound_manager.set_music_volume(new_volume)
                    update_config("music_volume", new_volume)

                if event.key == pg.K_UP and self.current_sound_volume_step < 10:
                    self.current_sound_volume_step += 1
                    new_sound_volume = self.current_sound_volume_step / 10
                    self.game.sound_manager.set_sound_volume(new_sound_volume)
                    update_config("sound_volume", new_sound_volume)

                if event.key == pg.K_DOWN and self.current_sound_volume_step > 0:
                    self.current_sound_volume_step -= 1
                    new_sound_volume = self.current_sound_volume_step / 10
                    self.game.sound_manager.set_sound_volume(new_sound_volume)
                    update_config("sound_volume", new_sound_volume)

                if event.key == pg.K_ESCAPE:
                    self.done = True
                    self.next_state = self.game.previous_state
                       
                if event.key == pg.K_s:
                    self.game.sound_manager.toggle_sound()                    

                if event.key == pg.K_m:
                    self.game.sound_manager.music_enabled = self.game.sound_manager.toggle_music()

                if event.key == pg.K_r:
                    self.pending_action = "reset_high_score"
                    self.show_confirmation = True
                
    
    def update(self, dt):
        self.animation_frame_time += dt * 1000
        if self.animation_frame_time > self.game.graphics_manager.highlight_delay:
            self.animation_frame_time = 0
            for icon in self.game.graphics_manager.arrows_list:
                icon.set_alpha(150)
            self.game.graphics_manager.arrows_list[self.game.graphics_manager.highlight_index].set_alpha(255)
            self.game.graphics_manager.highlight_index = (self.game.graphics_manager.highlight_index + 1) % 4
        # Check if the message timer has expired
        if self.high_score_reset_message:
            self.message_timer += dt * 1000
            if self.message_timer > MESSAGE_DISPLAY_TIME:
                self.high_score_reset_message = False  # Hide the message          
    
    def draw(self, surface):
        surface.blit(self.game.graphics_manager.background_image, (0, 0))
        self.draw_settings_menu(surface)
        if self.show_confirmation:
            draw_confirm_popup(surface, self.game)
    
    def draw_settings_menu(self, surface):
        scale_factor = self.game.scale_factor
        screen_width = self.game.screen_width
        screen_height = self.game.screen_height
        icon_x = screen_width * 0.37
        text_x = icon_x + screen_width * 0.05
        icon_y = screen_height * 2 / 5
        text_y = icon_y + screen_width * 0.026
        y_increment = 0.056 * screen_height

        draw_text(surface, "High Score: " + str(self.game.high_score), round(22 * scale_factor), screen_width * 0.5, screen_height * 0.02, self.game.font_name) 
        draw_text(surface, "SETTINGS", round(48 * scale_factor), screen_width * 0.5, screen_height * 0.25, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["s_icon"], icon_x, icon_y)
        draw_icon_text(surface, f"Sound: {"ON" if self.game.sound_manager.sound_enabled else "OFF"}", round(22 * scale_factor), text_x, text_y, self.game.font_name) 

        draw_icon(surface, self.game.graphics_manager.icons["m_icon"], icon_x, icon_y + y_increment)
        draw_icon_text(surface, f"Music: {"ON" if self.game.sound_manager.music_enabled else "OFF"}", round(22 * scale_factor), text_x, text_y + y_increment, self.game.font_name)

        draw_icon(surface, self.game.graphics_manager.icons["r_icon"], icon_x, icon_y + 2 * y_increment)
        draw_icon_text(surface, "Reset High Score", round(22 * scale_factor), text_x, text_y + 2 * y_increment, self.game.font_name)
        if self.high_score_reset_message:
            draw_text(surface, "High Score Reset!", round(22 * scale_factor), screen_width / 2, screen_height * 0.56, self.game.font_name, GREEN)

        block_width = int(15 / 576 * screen_width)
        block_height = 15 / 720 * screen_height
        block_spacing = 0
        icon_spacing = 5 / 576 * screen_width
        start_x = screen_width // 2 - (10 * (block_width + block_spacing)) // 2  # Center the row
        last_block_x = start_x + (11 * (block_width + block_spacing)) - 1.5 * block_spacing
        plus_x = last_block_x + 1.6 * icon_spacing
        minus_x = start_x - (block_width + icon_spacing)

        for i in range(1, 11):
            if i <= self.current_volume_step:
                color = GREEN  # Filled block for active volume
            else:
                color = GRAY   # Empty block for inactive
            # Draw a rectangle for each block
            block_rect = pg.Rect(start_x, screen_height * 3.4 / 5, block_width, block_height)
            pg.draw.rect(surface, color, block_rect)
            start_x += block_width + block_spacing

        start_x = screen_width // 2 - (10 * (block_width + block_spacing)) // 2  # Center the row
        last_sound_block_x = start_x + (11 * (block_width + block_spacing)) - 1.5 * block_spacing
        up_x = last_sound_block_x + 1.6 * icon_spacing
        down_x = start_x - (block_width + icon_spacing)

        for i in range(1, 11):
            if i <= self.current_sound_volume_step:
                color = GREEN  # Filled block for active volume
            else:
                color = GRAY   # Empty block for inactive
            # Draw a rectangle for each block
            block_rect = pg.Rect(start_x, screen_height * 3.85 / 5, block_width, block_height)
            pg.draw.rect(surface, color, block_rect)
            start_x += block_width + block_spacing

        draw_text(surface, f"Music Volume: {self.current_volume_step}", round(22 * scale_factor), screen_width // 2, screen_height * 3.15 / 5, self.game.font_name)
        draw_icon(surface, self.game.graphics_manager.icons["left_icon"], minus_x, screen_height * 3.35 / 5)
        draw_icon(surface, self.game.graphics_manager.icons["right_icon"], plus_x, screen_height * 3.35 / 5)

        draw_text(surface, f"Sound Volume: {self.current_sound_volume_step}", round(22 * scale_factor), screen_width // 2, screen_height * 3.6 / 5, self.game.font_name)
        draw_icon(surface, self.game.graphics_manager.icons["down_icon"], down_x, screen_height * 3.8 / 5)
        draw_icon(surface, self.game.graphics_manager.icons["up_icon"], up_x, screen_height * 3.8 / 5)

        draw_icon(surface, self.game.graphics_manager.icons["esc_icon"], screen_width * 0.07, screen_height * 0.92)
        draw_icon_text(surface, "Back", round(18 * scale_factor), screen_width * 0.11, screen_height * 0.940, self.game.font_name)

        # Draw animated arrows for game control tutorial
        draw_icon(surface, self.game.graphics_manager.icons["spacebar_icon"], screen_width * 0.92, screen_height * 0.92)
        draw_icon_text(surface, "Shoot", round(18 * scale_factor), screen_width * 0.78, screen_height * 0.940, self.game.font_name)

        arrow_x = screen_width * 0.945
        arrow_y = screen_height * 0.90
        arrow_spacing_x = 16 / 576 * screen_width
        arrow_spacing_y = 16 / 576 * screen_height

        draw_icon(surface, self.game.graphics_manager.arrows["right_icon"], arrow_x, arrow_y - arrow_spacing_y)
        draw_icon(surface, self.game.graphics_manager.arrows["left_icon"], arrow_x - 2 * arrow_spacing_x, arrow_y - arrow_spacing_y)
        draw_icon(surface, self.game.graphics_manager.arrows["up_icon"], arrow_x - arrow_spacing_x, arrow_y - 2 * arrow_spacing_y)
        draw_icon(surface, self.game.graphics_manager.arrows["down_icon"], arrow_x - arrow_spacing_x, arrow_y - arrow_spacing_y)
        draw_icon_text(surface, "Move", round(18 * scale_factor), screen_width * 0.78, screen_height * 0.89, self.game.font_name)