import pygame as pg
from settings import *

def draw_text(surf, text, size, x, y, font_name, colour=WHITE):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, player_mini_img):
    for i in range(lives):
        img_rect = player_mini_img.get_rect()
        img_rect.x = x + PLAYER_LIVES_ICON_SPACING * i
        img_rect.y = y
        surf.blit(player_mini_img, img_rect)