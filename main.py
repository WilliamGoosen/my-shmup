import pygame as pg
from os import path
from sys import exit
from random import random, choice
from settings import *
from sprites import Player, Starfield, Meteoroid, Explosion
from utilities import draw_text, draw_lives, draw_shield_bar, spawn_wave


img_dir = path.join(path.dirname(__file__), 'img')

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(FONT_NAME)

#player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert_alpha()
#bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()

def draw_game_over_title():
    draw_text(screen, "GAME OVER", 48, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "Score: " + str(score), 22, WIDTH / 2, HEIGHT / 2, font_name)
    draw_text(screen, "Press SPACE to play again", 18, WIDTH / 2, HEIGHT * 3 / 4, font_name)
    draw_text(screen, "Press ESC to Quit", 18, WIDTH / 2, HEIGHT * 3 / 4 + 40, font_name)

def new_star():
    s = Starfield()
    all_sprites.add(s)
    stars.add(s)

def spawn_starfield():
    spawn_wave(new_star, NUMBER_OF_STARS)

def new_meteroid(meteor_images):
    m = Meteoroid(meteor_images)
    all_sprites.add(m)
    meteors.add(m)

def spawn_meteoroid_wave(meteor_images):
    spawn_wave(new_meteroid, NUMBER_OF_METEOROIDS, meteor_images)

def clear_game_objects():
    for meteor in meteors:
        meteor.kill()
    for bullet in bullets:
        bullet.kill()


def reset_game():
    global score, game_state, life_gained, player, draw_game_over_screen

    game_state = "playing"
    draw_game_over_screen = False
    score = 0
    life_gained = 0

    all_sprites.empty()
    bullets.empty()
    meteors.empty()
    players.empty()
    stars.empty()

    clear_game_objects()

    player = Player(all_sprites, bullets, shoot_sound)
    all_sprites.add(player)
    players.add(player)

    spawn_starfield()
    spawn_meteoroid_wave(meteor_images)

# Load all game graphics
game_background_original = pg.image.load(path.join("img/", "starfield.png")).convert_alpha()
scale_factor = HEIGHT / game_background_original.get_height()
new_width = int(game_background_original.get_height() * scale_factor)
new_height = int(game_background_original.get_height() * scale_factor)
game_background_scaled = pg.transform.smoothscale(game_background_original, (new_width, new_height))

if new_width > WIDTH:
    crop_x = (new_width - WIDTH) // 2
    game_background = game_background_scaled.subsurface((crop_x, 0, WIDTH, HEIGHT))
else:
    game_background = game_background_scaled
# background__original_rect = background_original.get_rect()
player_image = pg.image.load(path.join("img/", "playerShip1_orange.png")).convert_alpha()
player_mini_image = pg.transform.scale(player_image, (25, 19))
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

# Load all game sounds
shoot_sound = pg.mixer.Sound(path.join("snd/", "Laser_Shoot2.wav"))
shoot_sound.set_volume(0.1)
# shield_sound = pg.mixer.Sound(path.join("snd/", "pow4.wav"))
# power_sound = pg.mixer.Sound(path.join("snd/", "pow5.wav"))
# life_up_sound = pg.mixer.Sound(path.join("snd/", "jingles_NES09.ogg"))
expl_sounds = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    expl_sounds.append(pg.mixer.Sound(path.join("snd/", snd)))
player_die_sound = pg.mixer.Sound(path.join("snd/", 'rumble1.ogg'))
# pg.mixer.music.load(path.join("snd/", 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
# pg.mixer.music.set_volume(0.1)


all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
stars = pg.sprite.Group()
meteors = pg.sprite.Group()
players = pg.sprite.Group()
reset_game()

running = True
while running:
    # --- EVENT HANDLING ---
    quit_event = False
    space_key_pressed = False
    esc_key_pressed = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit_event = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                space_key_pressed = True
            if event.key == pg.K_ESCAPE:
                esc_key_pressed = True

    if quit_event:
        running = False

    # --- GAME LOGIC & STATE UPDATES ---

    if game_state == "playing":
        keystate = pg.key.get_pressed()
        player.update_with_keystate(keystate)
        all_sprites.update()

        if player.just_respawned:        
            spawn_meteoroid_wave(meteor_images)
            player.rect.centerx = WIDTH /2
            player.rect.bottom = HEIGHT - PLAYER_START_Y_OFFSET
            player.just_respawned = False
    
        # check to see if a bullet hit a meteoroid
        hits = pg.sprite.groupcollide(meteors, bullets, True, True)
        for hit in hits:
            score += 62 - hit.radius
            hit_sound = choice(expl_sounds)
            hit_sound.play()
            hit_sound.set_volume(0.1)
            explosion = Explosion(hit.rect.center, 'large_explosion', explosion_animation)
            all_sprites.add(explosion)
            # if random() > 0.9:
            #     power = Power(hit.rect.center)
            #     all_sprites.add(power)
            #     powerups.add(power)
            new_meteroid(meteor_images)
        
        # check to see if a meteoroid hits the player
        hits = pg.sprite.spritecollide(player, meteors, True, pg.sprite.collide_circle)
        for hit in hits:
            hit_sound = expl_sounds[0]
            hit_sound.play()
            hit_sound.set_volume(0.1)
            player.power = 1
            player.shield -= hit.radius * 2
            explosion = Explosion(hit.rect.center, 'small_explosion', explosion_animation)
            all_sprites.add(explosion)
            new_meteroid(meteor_images)

            if player.shield <= 0:
                player_die_sound.play()
                player_die_sound.set_volume(0.1)
                death_explosion = Explosion(player.rect.center, 'player_explosion', explosion_animation)
                all_sprites.add(death_explosion)
                player.hide()
                clear_game_objects()
                player.lives -= 1
                player.shield = 100

        if player.lives == 0 and not death_explosion.alive():
            game_state = "game_over"

    elif game_state == "paused":
        pass

    elif game_state == "game_over":
        if space_key_pressed:
            reset_game()            
        if esc_key_pressed:
            running = False
        clock.tick(10)
        # for event in pg.event.get():
        #     if event.type == pg.KEYDOWN:
        #         if event.key == pg.K_SPACE:
        #             reset_game()
        #         elif event.key == pg.K_ESCAPE:
        #             running = False
        # clock.tick(10)
        # draw_game_over_screen = True
        # screen.blit(game_background, (0, 0))

    else:
        draw_game_over_screen = False

    # --- DRAWING SECTION ---

    if game_state == "game_over":
        screen.blit(game_background, (0, 0))
    else:
        screen.fill(BG_COLOUR)
    
    all_sprites.draw(screen)
    if game_state == "playing":
        draw_text(screen, "Score: " + str(score), 18, WIDTH / 2, 10, font_name, WHITE)
        draw_lives(screen, 5, 5, player.lives, player_mini_image)
        draw_shield_bar(screen, WIDTH - BAR_LENGTH - 5, 5, player.shield)

    if game_state == "game_over":
        draw_game_over_title()

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
