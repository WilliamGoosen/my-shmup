import pygame as pg
from sys import exit
from settings import *
from sprites import Player

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(FONT_NAME)

all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    screen.fill(BG_COLOUR)
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    keystate = pg.key.get_pressed()
    all_sprites.update(keystate)
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
