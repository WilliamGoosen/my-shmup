import pygame as pg
from os import path
from sys import exit
from random import random, choice, randint
from settings import *
from sprites import Player, Starfield, Meteoroid, Explosion, Powerup
from utilities import draw_text, draw_lives, draw_shield_bar, spawn_wave, draw_icon, draw_icon_text


img_dir = path.join(path.dirname(__file__), 'img')

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(FONT_NAME)

#player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert_alpha()
#bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()

def load_data():        
        # Create the full path to the high score file
        hs_file_path = HS_FILE

        # Check if the file exists first
        if path.exists(hs_file_path):
            # If it exists, open it and try to read the score
            try:
                with open(hs_file_path, 'r') as f:
                    high_score = int(f.read())
            except ValueError:
                # This happens if the file exists but is empty/corrupt (not a number)
                high_score = 0
        else:
            # If the file does NOT exist, set high score to 0
            high_score = 0
        return high_score

def new_high_score_check():
    global high_score
    # new_high score_achieved = False
    if score > high_score:
        high_score = score
        new_high_score_achieved = True
        with open(HS_FILE, "w") as f:
            f.write(str(score))
    else:
        new_high_score_achieved = False
    return new_high_score_achieved

def reset_high_score():
    global high_score, high_score_reset_message, message_timer
    high_score = 0
    with open(HS_FILE, 'w') as f:
        f.write('0')
    
    # Activate the message and set the timer
    high_score_reset_message = True
    message_timer = pg.time.get_ticks()  # Record the current time


def draw_start_title():
    draw_text(screen, "High Score: " + str(high_score), 22, WIDTH / 2, 15, font_name)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2, font_name)
    draw_text(screen, "Press SPACE to play", 18, WIDTH / 2, HEIGHT * 3 / 4, font_name)
    draw_text(screen, "Press ENTER to Open Settings", 18, WIDTH / 2, HEIGHT * 3 / 4 + 40, font_name)
    draw_text(screen, "Press ESC to Quit Game", 18, WIDTH / 2, HEIGHT * 3 / 4 + 80, font_name)

def draw_settings_menu():   
    draw_text(screen, "High Score: " + str(high_score), 22, WIDTH / 2, 15, font_name) 
    draw_text(screen, "SETTINGS", 48, WIDTH / 2, HEIGHT / 4, font_name)    
    draw_icon_text(screen, f"Sound: {"ON" if sound_enabled else "OFF"}", 22, WIDTH * 0.4, HEIGHT / 2.5, font_name)    
    draw_icon_text(screen, f"Music: {"ON" if music_enabled else "OFF"}", 22, WIDTH * 0.4, HEIGHT / 2.5 + 40, font_name)
    draw_icon_text(screen, "Back", 18, 72, HEIGHT * 0.925, font_name)
    draw_icon_text(screen, "R: Reset High Score", 22, WIDTH * 0.4, HEIGHT / 2.5 + 80, font_name)
    if high_score_reset_message:
        draw_text(screen, "High Score Reset!", 22, WIDTH/2, HEIGHT/2 + 130, font_name, GREEN)    

def draw_pause_menu():
    draw_text(screen, "PAUSED", 48, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "Press ESC to resume", 18, WIDTH / 2, HEIGHT * 3 / 4, font_name)
    draw_text(screen, "Press ENTER to Open Settings", 18, WIDTH / 2, HEIGHT * 3 / 4 + 40, font_name)
    draw_text(screen, "Press Q to Quit to Title", 18, WIDTH / 2, HEIGHT * 3 / 4 + 80, font_name)

def draw_game_over_title(new_high_score_achieved):
    draw_text(screen, "High Score: " + str(high_score), 22, WIDTH / 2, 15, font_name)
    draw_text(screen, "GAME OVER", 48, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "Score: " + str(score), 30, WIDTH / 2, HEIGHT / 2, font_name)
    draw_text(screen, "Press SPACE to play again", 18, WIDTH / 2, HEIGHT * 3 / 4, font_name)
    draw_text(screen, "Press Q to Quit to Title", 18, WIDTH / 2, HEIGHT * 3 / 4 + 40, font_name)
    if new_high_score_achieved:
        draw_text(screen, "NEW HIGH SCORE!", 22, WIDTH / 2, HEIGHT / 2 + 40, font_name, GREEN)
    

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
    for meteoroid in meteors:
        meteoroid.kill()
    for bullet in bullets:
        bullet.kill()
    for powerup in powerups:
        powerup.kill()


def start_game():
    global score, game_state, life_gained, player

    # game_state = "playing"
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
plus_icon = pg.image.load(path.join("img/", "tile_0062.png"))
plus_icon_scaled = pg.transform.scale_by(plus_icon, 32/16)
minus_icon = pg.image.load(path.join("img/", "tile_0061.png"))
minus_icon_scaled = pg.transform.scale_by(minus_icon, 32/16)
m_icon = pg.image.load(path.join("img/", "tile_0161.png"))
m_icon_scaled = pg.transform.scale_by(m_icon, 32/16)
q_icon = pg.image.load(path.join("img/", "tile_0085.png"))
q_icon_scaled = pg.transform.scale_by(q_icon, 32/16)
r_icon = pg.image.load(path.join("img/", "tile_0088.png"))
r_icon_scaled = pg.transform.scale_by(r_icon, 32/16)
s_icon = pg.image.load(path.join("img/", "tile_0121.png"))
s_icon_scaled = pg.transform.scale_by(s_icon, 32/16)
enter_icon = pg.image.load(path.join("img/", "enter.png")).convert_alpha()
enter_icon_scaled = pg.transform.scale_by(enter_icon,(32/20))
spacebar_icon = pg.image.load(path.join("img/", "spacebar.png")).convert_alpha()
spacebar_icon_scaled = pg.transform.scale_by(spacebar_icon,(32/16))
esc_icon = pg.image.load(path.join("img/", "tile_0017.png"))
esc_icon_scaled = pg.transform.scale_by(esc_icon, 32/16)

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

powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join("img/", 'shield_gold.png')).convert_alpha()
powerup_images['gun'] = pg.image.load(path.join("img/", 'bolt_gold.png')).convert_alpha()

# Load all game sounds
shoot_sound = pg.mixer.Sound(path.join("snd/", "Laser_Shoot2.wav"))
shoot_sound.set_volume(0.1)
shield_sound = pg.mixer.Sound(path.join("snd/", "pow4.wav"))
power_sound = pg.mixer.Sound(path.join("snd/", "pow5.wav"))
# life_up_sound = pg.mixer.Sound(path.join("snd/", "jingles_NES09.ogg"))
expl_sounds = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    expl_sounds.append(pg.mixer.Sound(path.join("snd/", snd)))
player_die_sound = pg.mixer.Sound(path.join("snd/", 'rumble1.ogg'))
pg.mixer.music.load(path.join("snd/", 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(loops=-1)


all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
stars = pg.sprite.Group()
meteors = pg.sprite.Group()
powerups = pg.sprite.Group()
players = pg.sprite.Group()

sound_enabled = True
music_enabled = True
game_state = "title"
previous_state = None
high_score_reset_message = False
message_timer = 0
high_score = load_data()

running = True
while running:
    # --- EVENT HANDLING ---
    quit_event = False
    space_key_pressed = False
    esc_key_pressed = False
    q_key_pressed = False
    r_key_pressed = False
    s_key_pressed = False
    m_key_pressed = False
    enter_key_pressed = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit_event = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                space_key_pressed = True
            if event.key == pg.K_ESCAPE:
                esc_key_pressed = True
            if event.key == pg.K_q:
                q_key_pressed = True
            if event.key == pg.K_s:
                s_key_pressed = True
            if event.key == pg.K_m:
                m_key_pressed = True
            if event.key == pg.K_RETURN:
                enter_key_pressed = True
            if event.key == pg.K_r:
                r_key_pressed = True

    if quit_event:
        running = False

    # --- GAME LOGIC & STATE UPDATES ---
    if game_state == "title":
        if space_key_pressed:
            start_game()
            game_state = "playing"
        if enter_key_pressed:
            previous_state = game_state
            game_state = "settings"
        if esc_key_pressed:
            running = False
        clock.tick(10)

    elif game_state == "settings":
        if esc_key_pressed:
            game_state = previous_state
        if s_key_pressed:
            sound_enabled = not sound_enabled
        if m_key_pressed:
            music_enabled = not music_enabled
            if music_enabled:
                pg.mixer.music.unpause()
            else:
                pg.mixer.music.pause()
        if r_key_pressed:
            reset_high_score()
        
        # Check if the message timer has expired
        if high_score_reset_message:
            now = pg.time.get_ticks()
            if now - message_timer > MESSAGE_DISPLAY_TIME:
                high_score_reset_message = False  # Hide the message

        clock.tick(10)
        
    elif game_state == "playing":
        if esc_key_pressed:
            game_state = "paused"
        keystate = pg.key.get_pressed()
        player.update_with_keystate(keystate, sound_enabled)
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
            if sound_enabled:
                hit_sound.play()
                hit_sound.set_volume(0.1)
            explosion = Explosion(hit.rect.center, 'large_explosion', explosion_animation)
            all_sprites.add(explosion)
            if random() < POWERUP_DROP_CHANCE:
                power = Powerup(powerup_images, hit.rect.center)
                all_sprites.add(power)
                powerups.add(power)
            new_meteroid(meteor_images)
        
        # check to see if a meteoroid hits the player
        hits = pg.sprite.spritecollide(player, meteors, True, pg.sprite.collide_circle)
        for hit in hits:
            hit_sound = expl_sounds[0]
            if sound_enabled:
                hit_sound.play()
                hit_sound.set_volume(0.1)
            player.power = 1
            player.shield -= hit.radius * 2
            explosion = Explosion(hit.rect.center, 'small_explosion', explosion_animation)
            all_sprites.add(explosion)
            new_meteroid(meteor_images)

            if player.shield <= 0:
                if sound_enabled:
                    player_die_sound.play()
                    player_die_sound.set_volume(0.1)
                death_explosion = Explosion(player.rect.center, 'player_explosion', explosion_animation)
                all_sprites.add(death_explosion)
                player.hide()
                clear_game_objects()
                player.lives -= 1
                player.shield = 100

        # check to see if player hit a powerup
        hits = pg.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += randint(10, 30)
                if sound_enabled:
                    shield_sound.play()
                    shield_sound.set_volume(0.2)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                if sound_enabled:
                    power_sound.play()
                    power_sound.set_volume(0.2)

        # if the player died and the explosion has finished playing
        if player.lives == 0 and not death_explosion.alive():
            game_state = "game_over"
            new_high_score_achieved = new_high_score_check()  

    elif game_state == "paused":
        if esc_key_pressed:
            game_state = "playing"
        if q_key_pressed:
            game_state = "title"
            # running = False
        if enter_key_pressed:
            previous_state = game_state
            game_state = "settings"
        all_sprites.draw(screen)        
        clock.tick(10)
        
    elif game_state == "game_over":        
        if space_key_pressed:
            start_game()
            game_state = "playing"            
        if q_key_pressed:
            # running = False
            game_state = "title"
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
    

    # --- DRAWING SECTION ---

    if game_state in ("title", "settings", "game_over"):
        screen.blit(game_background, (0, 0))
    # elif game_state == "game_over":
    #     screen.blit(game_background, (0, 0))
    else:
        screen.fill(BG_COLOUR)
    
    if game_state not in ("title", "settings"):
        all_sprites.draw(screen)

    if game_state == "title":
        draw_start_title()

    if game_state == "settings":
        draw_settings_menu()
        draw_icon(screen, s_icon_scaled, WIDTH * 0.33, HEIGHT/ 2.5 - 2)
        draw_icon(screen, m_icon_scaled, WIDTH * 0.33, HEIGHT/2.5 + 38)
        draw_icon(screen, r_icon_scaled, WIDTH * 0.33, HEIGHT/2.5 + 78)
        draw_icon(screen, esc_icon_scaled, WIDTH * 0.05, HEIGHT * 0.92)
        # draw_icon(screen, plus_icon_scaled, 100, HEIGHT - 100)
        # draw_icon(screen, minus_icon_scaled, 100, HEIGHT - 100)

    if game_state == "playing":
        draw_text(screen, "Score: " + str(score), 18, WIDTH / 2, 10, font_name, WHITE)
        draw_lives(screen, 5, 5, player.lives, player_mini_image)
        draw_shield_bar(screen, WIDTH - BAR_LENGTH - 5, 5, player.shield)
        
    if game_state == "paused":        
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        screen.blit(overlay, (0, 0))
        draw_text(screen, "Score: " + str(score), 18, WIDTH / 2, 10, font_name, WHITE)
        draw_lives(screen, 5, 5, player.lives, player_mini_image)
        draw_shield_bar(screen, WIDTH - BAR_LENGTH - 5, 5, player.shield)
        draw_pause_menu()
        

    if game_state == "game_over":        
        draw_game_over_title(new_high_score_achieved)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
