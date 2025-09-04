import pygame as pg
from os import path
from sys import exit
from settings import *
from sprites import Player, Starfield, Meteroid


img_dir = path.join(path.dirname(__file__), 'img')

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(FONT_NAME)

#player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert_alpha()
#bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()

def new_star():
    s = Starfield()
    all_sprites.add(s)
    stars.add(s)

def new_meteroid(meteor_images):
    m = Meteroid(meteor_images)
    all_sprites.add(m)
    meteors.add(m)

# Load all game graphics
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png',
               'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']
for img in meteor_list:
    img_surface = pg.image.load(path.join("img/", img)).convert_alpha()
    img_surface.set_colorkey(BLACK)
    meteor_images.append(img_surface)


all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
stars = pg.sprite.Group()
meteors = pg.sprite.Group()
players = pg.sprite.Group()
player = Player(all_sprites, bullets)
# all_sprites.add(player)
for _ in range(NUMBER_OF_STARS):
    new_star()

for _ in range(NUMBER_OF_METEOROIDS):
    new_meteroid(meteor_images)

running = True
while running:
    screen.fill(BG_COLOUR)
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    keystate = pg.key.get_pressed()
    player.update(keystate)
    # players.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    screen.blit(player.image, player.rect)
    
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
