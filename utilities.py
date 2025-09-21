import pygame as pg
from settings import *
from os import path
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game

def reset_high_score(game):    
    game.high_score = 0
    with open(HS_FILE, 'w') as f:
        f.write('0')

def load_config():
    config_dict = {}
    config_lines = load_or_create_file(CONFIG_FILE, 'scale_factor=1.0\nmusic_volume=0.5\nsound_volume=0.5').splitlines()

    for line in config_lines:
        if "=" in line:
            key, value = line.split("=", 1)
            config_dict[key] = value
    return config_dict
    
def update_config(key, new_value):
    config_dict = load_config()
    config_dict[key] = new_value
    lines = [f"{key}={value}" for key, value in config_dict.items()]
    with open(CONFIG_FILE, 'w') as f:
        f.write("\n".join(lines))

def load_or_create_file(file_path, default_value):
    # Check if the file exists first
    if path.exists(file_path):
        # If it exists, open it and try to read the score
        try:
            with open(file_path, 'r') as f:
                return f.read().strip()
        except ValueError:
            # If file is corrupt or disappears, fall back to default
            pass
    # If file doesn't exist or is invalid, create it with the default
    with open(file_path, 'w') as f:
        f.write(str(default_value))
    return default_value  # Return the default value

_text_cache = {}
_font_cache = {}

def draw_text(surf, text, size, x, y, font_name, colour=WHITE):
    # --- 1. CACHE THE FONT OBJECT ---
    # Create a key for the font (name + size)
    font_key = (font_name, size)
    if font_key not in _font_cache:
        _font_cache[font_key] = pg.font.Font(font_name, size)
    font = _font_cache[font_key]
    
    # --- 2. CACHE THE RENDERED TEXT SURFACE ---
    # Create a key for the specific text (font key + text + color)
    text_key = font_key + (text, colour)
    if text_key not in _text_cache:
        _text_cache[text_key] = font.render(text, True, colour)
    text_surface = _text_cache[text_key]
    
    # --- 3. BLIT THE PRE-RENDERED SURFACE (This is fast) ---
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_icon_text(surf, text, size, x, y, font_name, colour=WHITE):
    # --- 1. CACHE THE FONT OBJECT ---
    # Create a key for the font (name + size)
    font_key = (font_name, size)
    if font_key not in _font_cache:
        _font_cache[font_key] = pg.font.Font(font_name, size)
    font = _font_cache[font_key]
    
    # --- 2. CACHE THE RENDERED TEXT SURFACE ---
    # Create a key for the specific text (font key + text + color)
    text_key = font_key + (text, colour)
    if text_key not in _text_cache:
        _text_cache[text_key] = font.render(text, True, colour)
    text_surface = _text_cache[text_key]
    
    # --- 3. BLIT THE PRE-RENDERED SURFACE (This is fast) ---
    text_rect = text_surface.get_rect()
    text_rect.midleft = (x, y)
    surf.blit(text_surface, text_rect)
    
def clear_text_caches():
    """Call this if you need to reload fonts (e.g., on a resolution change)."""
    global _font_cache, _text_cache
    _font_cache.clear()
    _text_cache.clear()

def draw_icon(surf, image, x, y):
    """
    Blits an image (icon) onto a surface at the specified position.
    """
    icon_rect = image.get_rect()
    icon_rect.midtop = (x, y)
    surf.blit(image, icon_rect)


def draw_lives(surf: pg.Surface, game: 'Game', lives: int, player_mini_img: pg.Surface) -> None:
    lives_icon_spacing = PLAYER_LIVES_ICON_SPACING * game.scale_factor
    screen_edge_offset_x = 5 * game.scale_factor
    screen_edge_offset_y = 5 * game.scale_factor
    for i in range(lives):
        img_rect = player_mini_img.get_rect()
        img_rect.x = screen_edge_offset_x + lives_icon_spacing  * i
        img_rect.y = screen_edge_offset_y
        surf.blit(player_mini_img, img_rect)


def draw_health_bar(surf: pg.Surface, game: 'Game', percent: float) -> None:
    health_bar_length = BAR_LENGTH * game.scale_factor
    health_bar_height = BAR_HEIGHT * game.scale_factor
    screen_edge_offset_x = game.WIDTH - health_bar_length - 5 * game.scale_factor
    screen_edge_offset_y = 5 * game.scale_factor
    if percent < 0:
        percent = 0
    fill = (percent / 100) * health_bar_length
    outline_rect = pg.Rect(screen_edge_offset_x, screen_edge_offset_y, health_bar_length, health_bar_height)
    fill_rect = pg.Rect(screen_edge_offset_x, screen_edge_offset_y, fill, health_bar_height)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def spawn_wave(function_to_call, count, *args):
    """
    Calls a given function a specified number of times with provided arguments.

    Args:
        function_to_call (callable): The function to be called repeatedly.
        count (int): The number of times to call the function.
        *args: Variable-length argument list to pass to the function.
    """
    for _ in range(count):
        function_to_call(*args)

def draw_confirm_popup(surface, game):
    scale_factor = game.scale_factor

    surface.blit(game.graphics_manager.confirm_overlay, (0, 0))
    popup_rect = game.graphics_manager.popup_bg.get_rect(center = (game.WIDTH // 2, game.HEIGHT // 2))
    surface.blit(game.graphics_manager.popup_bg, popup_rect.topleft)

    draw_text(surface, "Are you sure?", round(24 * scale_factor), game.WIDTH * 0.5, game.HEIGHT * 0.45, game.font_name, WHITE)

    draw_icon(surface, game.graphics_manager.icons["y_icon"], game.WIDTH * 0.4, game.HEIGHT * 0.497)
    draw_text(surface, "Yes", round(24 * scale_factor), game.WIDTH * 0.455, game.HEIGHT * 0.497, game.font_name, WHITE)

    draw_icon(surface, game.graphics_manager.icons["n_icon"], game.WIDTH * 0.55, game.HEIGHT * 0.497)
    draw_text(surface, "No", round(24 * scale_factor), game.WIDTH * 0.60, game.HEIGHT * 0.497, game.font_name, WHITE)
