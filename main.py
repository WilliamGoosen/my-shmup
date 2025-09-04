import pygame as pg
from os import path
from sys import exit
from random import random
from settings import *
from sprites import Player, Starfield, Meteroid, Explosion


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

explosion_animation = {'large_explosion': [], 'small_explosion': [], 'player_explosion': [], 'boss_explosion': []}
for _ in range(9):
    filename = 'regularExplosion0{}.png'.format(_)
    img = pg.image.load(path.join("img/", filename)).convert_alpha()
    img.set_colorkey(BLACK)
    img_large = pg.transform.scale(img, (75, 75)).convert_alpha()
    explosion_animation['large_explosion'].append(img_large)
    img_small = pg.transform.scale(img, (60, 60)).convert_alpha()
    explosion_animation['small_explosion'].append(img_small)
    filename = 'sonicExplosion0{}.png'.format(_)
    img = pg.image.load(path.join("img/", filename)).convert_alpha()
    img.set_colorkey(BLACK)
    explosion_animation['player_explosion'].append(img)
    img_boss_explode = pg.transform.scale(img, (298, 302))
    explosion_animation['boss_explosion'].append(img_boss_explode)


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

score = 0


running = True
while running:
    keystate = pg.key.get_pressed()
    player.update(keystate)
    all_sprites.update()
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill(BG_COLOUR)
    all_sprites.draw(screen)
    screen.blit(player.image, player.rect)
    
        # check to see if a bullet hit a meteoroid
    hits = pg.sprite.groupcollide(meteors, bullets, True, True)
    for hit in hits:
        score += 62 - hit.radius
        # hit_sound = choice(expl_sounds)
        # hit_sound.play()
        # hit_sound.set_volume(0.2)
        explosion = Explosion(hit.rect.center, 'large_explosion', explosion_animation)
        all_sprites.add(explosion)
        # if random() > 0.9:
        #     power = Power(hit.rect.center)
        #     all_sprites.add(power)
        #     powerups.add(power)
        new_meteroid(meteor_images)
    
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
