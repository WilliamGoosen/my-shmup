import pygame as pg
from os import path
from settings import *
from sprites import Player, Starfield, Explosion
from game_logic import clear_game_objects, handle_bullet_meteoroid_collisions, handle_player_meteoroid_collisions, handle_player_powerup_collisions, handle_player_respawn, spawn_meteoroid_wave, new_high_score_check
from sound_manager import SoundManager
from graphics_manager import GraphicsManager
from utilities import draw_text, draw_lives, draw_shield_bar, spawn_wave, draw_icon, draw_icon_text, load_or_create_file, reset_high_score
from game import Game
from play_state import PlayState
from pause_state import PauseState


def load_config():
    config_dict = {}
    config_lines = load_or_create_file(CONFIG_FILE, 'scale_factor=1.0').splitlines()

    for line in config_lines:
        if "=" in line:
            key, value = line.split("=", 1)
            config_dict[key] = value
    return config_dict


def draw_start_title():
    icon_x = WIDTH * 0.40
    icon_text_padding_x = 0.06
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 0.7
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y

    draw_text(screen, "High Score: " + str(game.high_score), 22, WIDTH * 0.5, HEIGHT * 0.02, font_name)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4, font_name)

    draw_icon(screen, graphics_manager.icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, "Start Game", 22, text_x, text_y, font_name)

    draw_icon(screen, graphics_manager.icons["enter_icon"], WIDTH * 0.92, HEIGHT * 0.915)
    draw_icon_text(screen, "Settings", 18, WIDTH * 0.78, HEIGHT * 0.940, font_name) 

    draw_icon(screen, graphics_manager.icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)
    draw_icon_text(screen, "Quit Game", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)


def draw_settings_menu():
    icon_x = WIDTH * 0.37
    icon_text_padding_x = 0.05
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 2 / 5
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y
    y_increment = 40

    draw_text(screen, "High Score: " + str(game.high_score), 22, WIDTH * 0.5, HEIGHT * 0.02, font_name) 
    draw_text(screen, "SETTINGS", 48, WIDTH * 0.5, HEIGHT * 0.25, font_name)

    draw_icon(screen, graphics_manager.icons["s_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, f"Sound: {"ON" if sound_enabled else "OFF"}", 22, text_x, text_y, font_name) 

    draw_icon(screen, graphics_manager.icons["m_icon"], icon_x, icon_y + icon_text_padding_y + y_increment)
    draw_icon_text(screen, f"Music: {"ON" if music_enabled else "OFF"}", 22, text_x, text_y + y_increment, font_name)

    draw_icon(screen, graphics_manager.icons["r_icon"], icon_x, icon_y + icon_text_padding_y + 2 * y_increment)
    draw_icon_text(screen, "Reset High Score", 22, text_x, text_y + 2 * y_increment, font_name)
    if high_score_reset_message:
        draw_text(screen, "High Score Reset!", 22, WIDTH / 2, HEIGHT * 0.68, font_name, GREEN)

    draw_text(screen, f"Music Volume: {current_volume_step}", 22, WIDTH // 2, HEIGHT * 3 / 5, font_name)
    draw_text(screen, f"Sound Volume: {current_sound_volume_step}", 22, WIDTH // 2, HEIGHT * 3.6 / 5, font_name)
    
    block_width = int(15 / 576 * WIDTH)
    block_height = 15 / 720 * HEIGHT
    block_spacing = 0
    icon_spacing = 5 / 576 * WIDTH
    start_x = WIDTH // 2 - (10 * (block_width + block_spacing)) // 2  # Center the row
    last_block_x = start_x + (11 * (block_width + block_spacing)) - 1.5 * block_spacing
    plus_x = last_block_x + 1.6 * icon_spacing
    minus_x = start_x - (block_width + icon_spacing)

    for i in range(1, 11):
        if i <= current_volume_step:
            color = GREEN  # Filled block for active volume
        else:
            color = GRAY   # Empty block for inactive
        # Draw a rectangle for each block
        block_rect = pg.Rect(start_x, HEIGHT * 3.25 / 5, block_width, block_height)
        pg.draw.rect(screen, color, block_rect)
        start_x += block_width + block_spacing
        
    start_x = WIDTH // 2 - (10 * (block_width + block_spacing)) // 2  # Center the row
    last_sound_block_x = start_x + (11 * (block_width + block_spacing)) - 1.5 * block_spacing
    up_x = last_sound_block_x + 1.6 * icon_spacing
    down_x = start_x - (block_width + icon_spacing)
        
    for i in range(1, 11):
        if i <= current_sound_volume_step:
            color = GREEN  # Filled block for active volume
        else:
            color = GRAY   # Empty block for inactive
        # Draw a rectangle for each block
        block_rect = pg.Rect(start_x, HEIGHT * 3.85 / 5, block_width, block_height)
        pg.draw.rect(screen, color, block_rect)
        start_x += block_width + block_spacing


    draw_icon(screen, graphics_manager.icons["left_icon"], minus_x, HEIGHT * 3.2 / 5)
    draw_icon(screen, graphics_manager.icons["right_icon"], plus_x, HEIGHT * 3.2 / 5)
    
    draw_icon(screen, graphics_manager.icons["down_icon"], down_x, HEIGHT * 3.8 / 5)
    draw_icon(screen, graphics_manager.icons["up_icon"], up_x, HEIGHT * 3.8 / 5)

    draw_icon(screen, graphics_manager.icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)
    draw_icon_text(screen, "Back", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)

    draw_icon(screen, graphics_manager.icons["spacebar_icon"], WIDTH * 0.92, HEIGHT * 0.92)
    draw_icon_text(screen, "Shoot", 18, WIDTH * 0.78, HEIGHT * 0.940, font_name)

    arrow_x = WIDTH * 0.945
    arrow_y = HEIGHT * 0.90
    draw_icon(screen, graphics_manager.arrows["right_icon"], arrow_x, arrow_y - 16)
    draw_icon(screen, graphics_manager.arrows["left_icon"], arrow_x - 2 * 16, arrow_y - 16)
    draw_icon(screen, graphics_manager.arrows["up_icon"], arrow_x - 16, arrow_y - 2 * 16)
    draw_icon(screen, graphics_manager.arrows["down_icon"], arrow_x - 16, arrow_y - 16)
    draw_icon_text(screen, "Move", 18, WIDTH * 0.78, HEIGHT * 0.89, font_name)


def draw_pause_menu():
    icon_x = WIDTH * 0.42
    icon_text_padding_x = 0.06
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 0.7
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y

    draw_text(screen, "PAUSED", 48, WIDTH / 2, HEIGHT / 4, font_name)

    draw_icon(screen, graphics_manager.icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, "Resume", 22, text_x, text_y, font_name)

    draw_icon(screen, graphics_manager.icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)
    draw_icon_text(screen, "Quit to Title", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)

    draw_icon(screen, graphics_manager.icons["enter_icon"], WIDTH * 0.92, HEIGHT * 0.915)
    draw_icon_text(screen, "Settings", 18, WIDTH * 0.78, HEIGHT * 0.940, font_name)

def draw_confirm_popup():

    screen.blit(graphics_manager.confirm_overlay, (0, 0))
    popup_rect = graphics_manager.popup_bg.get_rect(center = (WIDTH // 2, HEIGHT // 2))
    screen.blit(graphics_manager.popup_bg, popup_rect.topleft)

    draw_text(screen, "Are you sure?", 24, WIDTH * 0.5, HEIGHT * 0.45, font_name, WHITE)

    draw_icon(screen, graphics_manager.icons["y_icon"], WIDTH * 0.4, HEIGHT * 0.497)
    draw_text(screen, "Yes", 22, WIDTH * 0.45, HEIGHT * 0.5, font_name, WHITE)

    draw_icon(screen, graphics_manager.icons["n_icon"], WIDTH * 0.55, HEIGHT * 0.497)
    draw_text(screen, "No", 22, WIDTH * 0.60, HEIGHT * 0.5, font_name, WHITE)


def draw_game_over_title(new_high_score_achieved):
    icon_x = WIDTH * 0.42
    icon_text_padding_x = 0.06
    text_x = icon_x + WIDTH * icon_text_padding_x
    icon_y = HEIGHT * 0.7
    icon_text_padding_y = 0.026
    text_y = icon_y + WIDTH * icon_text_padding_y
    y_increment = 40

    draw_text(screen, "High Score: " + str(game.high_score), 22, WIDTH / 2, 15, font_name)
    draw_text(screen, "GAME OVER", 48, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "Score: " + str(game.score), 30, WIDTH / 2, HEIGHT * 2 / 5 + y_increment, font_name)

    if new_high_score_achieved:
        draw_text(screen, "NEW HIGH SCORE!", 30, WIDTH / 2, HEIGHT * 2 / 5, font_name, GREEN)

    draw_icon(screen, graphics_manager.icons["spacebar_icon"], icon_x, icon_y + icon_text_padding_y)
    draw_icon_text(screen, "Try Again", 22, text_x, text_y, font_name)   

    draw_icon(screen, graphics_manager.icons["esc_icon"], WIDTH * 0.07, HEIGHT * 0.92)
    draw_icon_text(screen, "Quit to Title", 18, WIDTH * 0.11, HEIGHT * 0.940, font_name)

    draw_icon(screen, graphics_manager.icons["q_icon"], WIDTH * 0.93, HEIGHT * 0.92)
    draw_icon_text(screen, "Quit Game", 18, WIDTH * 0.770, HEIGHT * 0.940, font_name)


def new_star():
    s = Starfield(WIDTH, HEIGHT)
    all_sprites_group.add(s)
    stars_group.add(s)

def spawn_starfield():
    spawn_wave(new_star, NUMBER_OF_STARS)

def start_game():
    global score, game_state, life_gained, player

    score = 0
    life_gained = 0

    all_sprites_group.empty()
    bullets_group.empty()
    meteors_group.empty()
    players_group.empty()
    stars_group.empty()

    clear_game_objects(meteors_group, bullets_group, powerups_group)

    player = Player(
        all_sprites_group,
        bullets_group,
        WIDTH,
        HEIGHT,
        sound_manager,
        graphics_manager.player_image)
    game.player = player
    player.bullet_image = graphics_manager.bullet_image
    all_sprites_group.add(player)
    players_group.add(player)

    spawn_starfield()
    spawn_meteoroid_wave(graphics_manager.meteoroid_images, WIDTH, HEIGHT, all_sprites_group, meteors_group)

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

# --- Load all game graphics ---
graphics_manager = GraphicsManager(scale_factor)

# --- Load all game sounds ---
sound_manager = SoundManager()


all_sprites_group = pg.sprite.Group()
bullets_group = pg.sprite.Group()
stars_group = pg.sprite.Group()
meteors_group = pg.sprite.Group()
powerups_group = pg.sprite.Group()
players_group = pg.sprite.Group()

sound_enabled = True
music_enabled = True
current_volume_step = int(sound_manager.music_volume * 10)
current_sound_volume_step = int(sound_manager.sound_volume * 10)
game_state = "title"
previous_state = None
high_score_reset_message = False
message_timer = 0
high_score = int(load_or_create_file(HS_FILE, 0))
show_confirmation = False
pending_action = None

# --- Create the Game object and populate it ---
game = Game()
game.graphics_manager = graphics_manager
game.sound_manager = sound_manager
game.all_sprites_group = all_sprites_group
game.bullets_group = bullets_group
game.stars_group = stars_group
game.meteors_group = meteors_group
game.powerups_group = powerups_group
game.players_group = players_group
game.WIDTH = WIDTH
game.HEIGHT = HEIGHT
game.BG_COLOUR = BG_COLOUR
game.font_name = font_name
game.high_score = high_score


running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Returns milliseconds, convert to seconds    
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
    plus_key_pressed = False
    minus_key_pressed = False
    up_key_pressed = False
    down_key_pressed = False
    left_key_pressed = False
    right_key_pressed = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit_event = True
        if event.type == pg.KEYDOWN:
            if game.current_state is None:
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
                if event.key == pg.K_RIGHT:
                    right_key_pressed = True
                if event.key == pg.K_LEFT:
                    left_key_pressed = True
                if event.key == pg.K_UP:
                    up_key_pressed = True
                if event.key == pg.K_DOWN:
                    down_key_pressed = True
            else:
                pass

            if game.current_state is not None:
                game.current_state.get_event(event)

    if game.current_state is not None:        
        game.current_state.update(dt)

        if game.current_state.done:
            return_state = game.current_state.return_state

            if game.current_state.next_state == "GAME_OVER":
                game_state = "game_over"
                game.current_state = None

            elif game.current_state.next_state == "PAUSE":
                # game_state = "paused"
                game.current_state = PauseState(game)
                game.current_state.startup()
                game_state = "paused"

            elif game.current_state.next_state == "PLAY":
                game.current_state = PlayState(game)
                game.current_state.startup()

            elif game.current_state.next_state == "TITLE":
                game_state = "title"
                game.current_state = None           

            elif game.current_state.next_state == "SETTINGS":
                game.current_state = None
                game_state = "settings"
                if return_state == "PAUSE":
                    previous_state = "paused"
                elif return_state == "TITLE":
                    previous_state = "title"                                   
                
            elif game.current_state.next_state == "RETURN_FROM_SETTINGS":                
                if previous_state == "paused":
                    game.current_state = PauseState(game)
                    game.current_state.startup()
                    game_state = "paused"
                elif game.previous_state == "TITLE":                    
                    pass
                game.current_state.startup()
                game_state = game.previous_state            

    if quit_event:
        running = False

    if show_confirmation:
            if y_key_pressed:
                if pending_action == "quit_to_title":
                    game_state = "title"
                elif pending_action == "reset_high_score":
                    reset_high_score(game)
                    high_score_reset_message = True
                    message_timer = pg.time.get_ticks()
                elif pending_action == "quit_game":
                    running = False

                show_confirmation = False
                pending_action = None

            elif n_key_pressed or esc_key_pressed:
                show_confirmation = False
                pending_action = None

    # --- GAME LOGIC & STATE UPDATES ---
    else:
        if game_state == "title":
            if space_key_pressed:
                start_game()
                game_state = "playing"
                # 1. Create a new PlayState, passing it the real game object
                new_play_state = PlayState(game)
                # 2. Initialize it for a new game
                new_play_state.startup()
                # 3. THIS IS THE KEY: Set the game's state to the new PlayState.
                #    This will be the signal for your main loop to use it.
                game.current_state = new_play_state
            if enter_key_pressed:
                previous_state = game_state
                game_state = "settings"
            if esc_key_pressed:
                running = False

        elif game_state == "settings":
            if right_key_pressed and current_volume_step < 10:
                current_volume_step += 1
                new_volume = current_volume_step / 10
                sound_manager.set_music_volume(new_volume)
            if left_key_pressed and current_volume_step > 0:
                current_volume_step -= 1
                new_volume = current_volume_step / 10
                sound_manager.set_music_volume(new_volume)
            if up_key_pressed and current_sound_volume_step < 10:
                current_sound_volume_step += 1
                new_sound_volume = current_sound_volume_step / 10
                sound_manager.set_sound_volume(new_sound_volume)
            if down_key_pressed and current_sound_volume_step > 0:
                current_sound_volume_step -= 1
                new_sound_volume = current_sound_volume_step / 10
                sound_manager.set_sound_volume(new_sound_volume)
            if esc_key_pressed:
                game_state = previous_state

                if previous_state == "paused":
                    game.current_state = PauseState(game)
                    game.current_state.startup()
                                    
            if s_key_pressed:
                sound_enabled = not sound_enabled
                sound_manager.set_sound_volume(1.0 if sound_enabled else 0.0)
            if m_key_pressed:
                music_enabled = sound_manager.toggle_music()
            if r_key_pressed:
                pending_action = "reset_high_score"
                show_confirmation = True
            now = pg.time.get_ticks()
            if now - graphics_manager.last_highlight_time > graphics_manager.highlight_delay:
                graphics_manager.last_highlight_time = now
                for icon in graphics_manager.arrows_list:
                    icon.set_alpha(150)
                graphics_manager.arrows_list[graphics_manager.highlight_index].set_alpha(255)
                graphics_manager.highlight_index = (graphics_manager.highlight_index + 1) % 4
            # Check if the message timer has expired
            if high_score_reset_message:
                now = pg.time.get_ticks()
                if now - message_timer > MESSAGE_DISPLAY_TIME:
                    high_score_reset_message = False  # Hide the message       

        elif game_state == "game_over":
            if space_key_pressed:
                start_game()
                game_state = "playing"
            if q_key_pressed:
                pending_action = "quit_game"
                show_confirmation = True
            if esc_key_pressed:
                game_state = "title"    

    # --- DRAWING SECTION ---

    if game_state in ("title", "settings", "game_over"):
        screen.blit(graphics_manager.background_image, (0, 0))
    else:
        screen.fill(BG_COLOUR)
        
    # --- MORE NEW CODE: Add this block here in the drawing section ---
    if game.current_state is not None:        
        # Let the current state draw itself
        game.current_state.draw(screen)
    else:
        if game_state not in ("title", "settings", "game_over"):
            all_sprites_group.draw(screen)

        if game_state == "title":
            draw_start_title()

        if game_state == "settings":
            draw_settings_menu()
            if show_confirmation:
                draw_confirm_popup()       

        if game_state == "game_over":
            draw_game_over_title(game.new_high_score_achieved)
            if show_confirmation:
                draw_confirm_popup()

    pg.display.flip()
pg.quit()
