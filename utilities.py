import pygame as pg
from settings import *

def draw_text(surf, text, size, x, y, font_name, colour=WHITE):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_icon_text(surf, text, size, x, y, font_name, colour=WHITE):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)

def draw_icon(surf, image, x, y):
    """
    Blits an image (icon) onto a surface at the specified position.
    """
    icon_rect = image.get_rect()
    icon_rect.topleft = (x, y)
    surf.blit(image, icon_rect)


def draw_lives(surf, x, y, lives, player_mini_img):
    for i in range(lives):
        img_rect = player_mini_img.get_rect()
        img_rect.x = x + PLAYER_LIVES_ICON_SPACING * i
        img_rect.y = y
        surf.blit(player_mini_img, img_rect)


def draw_shield_bar(surf, x, y, percent):
    if percent < 0:
        percent = 0
    fill = (percent / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
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