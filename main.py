import pygame as pg
from os import path
from sys import exit
from settings import *
from sprites import Player

img_dir = path.join(path.dirname(__file__), 'img')

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(FONT_NAME)

#player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert_alpha()
#bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()

all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
player = Player(all_sprites, bullets)
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
