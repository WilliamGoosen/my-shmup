import pygame as pg
from settings import *

def draw_text(surf, text, size, x, y, font_name, colour=WHITE):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)