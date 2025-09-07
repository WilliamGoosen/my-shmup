import pygame as pg
from os import path
from sys import exit
from random import random, choice, randint
from settings import *
from sprites import Player, Starfield, Meteoroid, Explosion, Powerup
from utilities import draw_text, draw_lives, draw_shield_bar, spawn_wave, draw_icon, draw_icon_text, load_or_create_file

# player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert_alpha()
# bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()

# def load_data():
#         # Create the full path to the high score file
#         hs_file_path = HS_FILE

#         # Check if the file exists first
#         if path.exists(hs_file_path):
#             # If it exists, open it and try to read the score
#             try:
#                 with open(hs_file_path, 'r') as f:
#                     high_score = int(f.read())
#             except ValueError:
#                 # This happens if the file exists but is empty/corrupt (not a number)
#                 high_score = 0
#         else:
#             # If the file does NOT exist, set high score to 0
#             high_score = 0
#         return high_score

def load_config():
    config_dict = {}
    config_lines = load_or_create_file(CONFIG_FILE, 'scale_factor=1.0').splitlines()

    for line in config_lines:
        if "=" in line:
            key, value = line.split("=", 1)
            config_dict[key] = value
    return config_dict

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
    icon_x = WIDTH * 0.40
    icon_text_padding_x = 0.06
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 0.7
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y
    y_increment = 40

    draw_text(screen, "High Score: " + str(high_score), 22, WIDTH * 0.5, HEIGHT * 0.02, font_name)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4, font_name)

    # draw_icon(screen, icons["enter_icon"], icon_x, icon_y + icon_text_padding_y)
    # draw_icon_text(screen, "Settings", 22, text_x, text_y, font_name)

    draw_icon(screen, icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, "Start Game", 22, text_x, text_y, font_name)

    draw_icon(screen, icons["enter_icon"], WIDTH * 0.92, HEIGHT * 0.915)
    draw_icon_text(screen, "Settings", 18, WIDTH * 0.78, HEIGHT * 0.940, font_name) 

    draw_icon(screen, icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)
    draw_icon_text(screen, "Quit Game", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)    


def draw_settings_menu():
    icon_x = WIDTH * 0.37
    icon_text_padding_x = 0.05
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 2 / 5
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y
    y_increment = 40

    draw_text(screen, "High Score: " + str(high_score), 22, WIDTH * 0.5, HEIGHT * 0.02, font_name) 
    draw_text(screen, "SETTINGS", 48, WIDTH * 0.5, HEIGHT * 0.25, font_name)

    draw_icon(screen, icons["s_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, f"Sound: {"ON" if sound_enabled else "OFF"}", 22, text_x, text_y, font_name) 

    draw_icon(screen, icons["m_icon"], icon_x, icon_y + icon_text_padding_y + y_increment)
    draw_icon_text(screen, f"Music: {"ON" if music_enabled else "OFF"}", 22, text_x, text_y + y_increment, font_name)

    draw_icon(screen, icons["r_icon"], icon_x, icon_y + icon_text_padding_y + 2 * y_increment)
    draw_icon_text(screen, "Reset High Score", 22, text_x, text_y + 2 * y_increment, font_name)
    if high_score_reset_message:
        draw_text(screen, "High Score Reset!", 22, WIDTH/2, HEIGHT * 0.68, font_name, GREEN)

    draw_icon(screen, icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)    
    draw_icon_text(screen, "Back", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)

    draw_icon(screen, icons["spacebar_icon"], WIDTH * 0.92, HEIGHT * 0.92)
    draw_icon_text(screen, "Shoot", 18, WIDTH * 0.78, HEIGHT * 0.940, font_name)

    arrow_x = WIDTH * 0.945
    arrow_y = HEIGHT * 0.90
    draw_icon(screen, arrows["right_icon"], arrow_x, arrow_y - 16)
    draw_icon(screen, arrows["left_icon"], arrow_x - 2 * 16, arrow_y - 16)
    draw_icon(screen, arrows["up_icon"], arrow_x - 16, arrow_y - 2 * 16)
    draw_icon(screen, arrows["down_icon"], arrow_x - 16, arrow_y - 16)
    # draw_icon_text(screen, "Quit Game", 18, WIDTH * 0.770, HEIGHT * 0.940, font_name)
    draw_icon_text(screen, "Move", 18, WIDTH * 0.78, HEIGHT * 0.89, font_name)


def draw_pause_menu():
    icon_x = WIDTH * 0.42
    icon_text_padding_x = 0.06
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 0.7
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y    
    y_increment = 40

    draw_text(screen, "PAUSED", 48, WIDTH / 2, HEIGHT / 4, font_name)    

    draw_icon(screen, icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, "Resume", 22, text_x, text_y, font_name)
    
    draw_icon(screen, icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)    
    draw_icon_text(screen, "Quit to Title", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)

    draw_icon(screen, icons["enter_icon"], WIDTH * 0.92, HEIGHT * 0.915)
    draw_icon_text(screen, "Settings", 18, WIDTH * 0.78, HEIGHT * 0.940, font_name)

def draw_confirm_popup():    

    screen.blit(confirm_overlay, (0, 0))
    popup_rect = popup_bg.get_rect(center = (WIDTH // 2, HEIGHT // 2))    
    screen.blit(popup_bg, popup_rect.topleft)

    draw_text(screen, "Are you sure?", 24, WIDTH * 0.5, HEIGHT * 0.45, font_name, WHITE)

    draw_icon(screen, icons["y_icon"], WIDTH * 0.4, HEIGHT * 0.497)   
    draw_text(screen, "Yes", 22, WIDTH * 0.45, HEIGHT * 0.5, font_name, WHITE)

    draw_icon(screen, icons["n_icon"], WIDTH * 0.55, HEIGHT * 0.497)   
    draw_text(screen, "No", 22, WIDTH * 0.60, HEIGHT * 0.5, font_name, WHITE)


def draw_game_over_title(new_high_score_achieved):
    icon_x = WIDTH * 0.42
    icon_text_padding_x = 0.06
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 0.7
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y    
    y_increment = 40

    draw_text(screen, "High Score: " + str(high_score), 22, WIDTH / 2, 15, font_name)
    draw_text(screen, "GAME OVER", 48, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "Score: " + str(score), 30, WIDTH / 2, HEIGHT * 2 / 5 + y_increment, font_name)
        
    if new_high_score_achieved:
        draw_text(screen, "NEW HIGH SCORE!", 30, WIDTH / 2, HEIGHT * 2 / 5, font_name, GREEN)

    draw_icon(screen, icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, "Try Again", 22, text_x, text_y, font_name)   
    # draw_text(screen, "Press SPACE to play again", 18, WIDTH / 2, HEIGHT * 3 / 4, font_name)

    draw_icon(screen, icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)    
    draw_icon_text(screen, "Quit to Title", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)

    draw_icon(screen, icons["q_icon"], WIDTH * 0.93, HEIGHT * 0.92)
    draw_icon_text(screen, "Quit Game", 18, WIDTH * 0.770, HEIGHT * 0.940, font_name)


def new_star():
    s = Starfield(WIDTH, HEIGHT)
    all_sprites.add(s)
    stars.add(s)

def spawn_starfield():
    spawn_wave(new_star, NUMBER_OF_STARS)

def new_meteroid(meteor_images):
    m = Meteoroid(meteor_images, WIDTH, HEIGHT)
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
    # draw_game_over_screen = False
    score = 0
    life_gained = 0

    all_sprites.empty()
    bullets.empty()
    meteors.empty()
    players.empty()
    stars.empty()

    clear_game_objects()

    player = Player(all_sprites, bullets, shoot_sound, WIDTH, HEIGHT)
    all_sprites.add(player)
    players.add(player)

    spawn_starfield()
    spawn_meteoroid_wave(meteor_images)

# Constants and initialisation
config = load_config()
scale_factor = float(config.get("scale_factor", 1.0))
music_volume = float(config.get("music_volume", 0.1))
WIDTH = int(BASE_WIDTH * scale_factor)
HEIGHT = int(BASE_HEIGHT * scale_factor)
img_dir = path.join(path.dirname(__file__), 'img')

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(FONT_NAME)

# Load all game graphics

confirm_overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
confirm_overlay.fill(CONFIRM_OVERLAY)
popup_width = WIDTH * 0.4
popup_height = HEIGHT * 0.2
popup_bg = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
popup_bg.fill(RED)

def load_icons(scale_factor):
    images = {}
    icon_list = [
        "enter_icon.png",
        "spacebar_icon.png",
        "spacebar_icon_2.png",
        "esc_icon.png",
        "minus_icon.png",
        "plus_icon.png",
        "m_icon.png",
        "q_icon.png",
        "r_icon.png",
        "s_icon.png",
        "y_icon.png",
        "n_icon.png"
    ]
    for file in icon_list:
        key = path.splitext(file)[0]
        # print(repr(key))
        icon = pg.image.load(path.join("img/", file)).convert_alpha()
        icon_factor = 2
        if key == "enter_icon":
            icon_factor = 4 / 3
        images[key] = pg.transform.scale_by(icon, icon_factor * scale_factor)        
    return images

icons = load_icons(scale_factor)

def load_arrows(scale_factor):
    images = {}
    icon_list = [
        "up_icon.png",
        "right_icon.png",
        "down_icon.png",
        "left_icon.png"        
    ]
    for file in icon_list:
        key = path.splitext(file)[0]
        # print(repr(key))
        icon = pg.image.load(path.join("img/", file)).convert_alpha()
        icon.set_alpha(150)
        icon_factor = 1.5      
        images[key] = pg.transform.scale_by(icon, icon_factor * scale_factor)        
    return images

arrows = load_arrows(scale_factor)
arrows_list = [arrows["up_icon"], arrows["down_icon"], arrows["left_icon"], arrows["right_icon"]]
highlight_index = 0
last_highlight_time = 0
highlight_delay = 600

def scale_background(WIDTH, HEIGHT):
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
    return game_background

game_background = scale_background(WIDTH, HEIGHT)
# background__original_rect = background_original.get_rect()
player_image = pg.image.load(path.join("img/", "playerShip1_orange.png")).convert_alpha()
player_mini_image = pg.transform.scale(player_image, (25, 19))

def load_meteors():
    meteor_images = []
    meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png',
               'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']
    for img in meteor_list:
        img_surface = pg.image.load(path.join("img/", img)).convert_alpha()
        img_surface.set_colorkey(BLACK)
        meteor_images.append(img_surface)
    return meteor_images

meteor_images = load_meteors()

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
high_score = int(load_or_create_file(HS_FILE, 0))
show_confirmation = False
pending_action = None

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
    y_key_pressed = False
    n_key_pressed = False

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
            if event.key == pg.K_y:
                y_key_pressed = True
            if event.key == pg.K_n:
                n_key_pressed = True

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
        
        now = pg.time.get_ticks()
        if now - last_highlight_time > highlight_delay:
            last_highlight_time = now

            for icon in arrows_list:
                icon.set_alpha(150)

            arrows_list[highlight_index].set_alpha(255)
            highlight_index = (highlight_index + 1) % 4
        
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
                power = Powerup(powerup_images, hit.rect.center, WIDTH, HEIGHT)
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
            new_high_score_achieved = int(new_high_score_check())

    elif game_state == "paused":
        if show_confirmation:
            if y_key_pressed:
                game_state = "title"
                show_confirmation = False
            elif n_key_pressed or esc_key_pressed:
                show_confirmation = False
        else:
            if space_key_pressed:
                game_state = "playing"
            if esc_key_pressed:
                pending_action = "title"
                show_confirmation = True                
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
            running = False
        if esc_key_pressed:
            game_state = "title"
        clock.tick(10)    

    # --- DRAWING SECTION ---

    if game_state in ("title", "settings", "game_over"):
        screen.blit(game_background, (0, 0))
    # elif game_state == "game_over":
    #     screen.blit(game_background, (0, 0))
    else:
        screen.fill(BG_COLOUR)
    
    if game_state not in ("title", "settings", "game_over"):
        all_sprites.draw(screen)

    if game_state == "title":
        draw_start_title()

    if game_state == "settings":
        draw_settings_menu()       

    if game_state == "playing":
        draw_text(screen, "Score: " + str(score), 22, WIDTH / 2, HEIGHT * 0.01, font_name, WHITE)
        draw_lives(screen, 5, 5, player.lives, player_mini_image)
        draw_shield_bar(screen, WIDTH - BAR_LENGTH - 5, 5, player.shield)
        
    if game_state == "paused":        
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        screen.blit(overlay, (0, 0))
        draw_text(screen, "Score: " + str(score), 22, WIDTH / 2, HEIGHT * 0.01, font_name, WHITE)
        draw_lives(screen, 5, 5, player.lives, player_mini_image)
        draw_shield_bar(screen, WIDTH - BAR_LENGTH - 5, 5, player.shield)
        draw_pause_menu()
        if show_confirmation:
            draw_confirm_popup()        

    if game_state == "game_over":        
        draw_game_over_title(new_high_score_achieved)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
