import pygame as pg
from os import path
from settings import *
from sprites import Starfield
from player import Player
from systems import SoundManager, GraphicsManager, game_logic
from utilities import spawn_wave, load_or_create_file
from game import Game
from states import PlayState, PauseState, TitleState, GameOverState, SettingsState

def load_config():
    config_dict = {}
    config_lines = load_or_create_file(CONFIG_FILE, 'scale_factor=1.0').splitlines()

    for line in config_lines:
        if "=" in line:
            key, value = line.split("=", 1)
            config_dict[key] = value
    return config_dict

def new_star():
    s = Starfield(WIDTH, HEIGHT)
    game.all_sprites_group.add(s)
    game.stars_group.add(s)

def spawn_starfield():
    spawn_wave(new_star, NUMBER_OF_STARS)

def start_game():
    global score, game_state, life_gained, player

    score = 0
    game.score = 0
    life_gained = 0

    game.all_sprites_group.empty()
    game.bullets_group.empty()
    game.meteors_group.empty()
    game.players_group.empty()
    game.stars_group.empty()

    game_logic.clear_game_objects(game.meteors_group, game.bullets_group, game.powerups_group)

    # player = Player(game)
    game.player = Player(game)
    game.player.bullet_image = game.graphics_manager.bullet_image
    game.all_sprites_group.add(game.player)
    game.players_group.add(game.player)

    spawn_starfield()
    game_logic.spawn_meteoroid_wave(game.graphics_manager.meteoroid_images, WIDTH, HEIGHT, game.all_sprites_group, game.meteors_group)

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


# --- Create the Game object and populate it ---
game = Game()
game.graphics_manager = GraphicsManager(scale_factor)
game.sound_manager = SoundManager()
game.all_sprites_group = pg.sprite.Group()
game.bullets_group = pg.sprite.Group()
game.stars_group = pg.sprite.Group()
game.meteors_group = pg.sprite.Group() 
game.powerups_group = pg.sprite.Group()
game.players_group = pg.sprite.Group()
game.WIDTH = WIDTH
game.HEIGHT = HEIGHT
game.BG_COLOUR = BG_COLOUR
game.font_name = pg.font.match_font(FONT_NAME)
game.high_score = int(load_or_create_file(HS_FILE, 0))
game.current_state = TitleState(game)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Returns milliseconds, convert to seconds

    # --- EVENT HANDLING ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
           
            running = False
 
        game.current_state.get_event(event)

   
    game.current_state.update(dt)

    if game.current_state.done:
        if game.current_state.quit:
            running = False
            continue
        return_state = game.current_state.return_state
        if game.current_state.next_state == "GAME_OVER":
            game.current_state = GameOverState(game)
        elif game.current_state.next_state == "PAUSE":
            game.current_state = PauseState(game)
            game_state = "paused"
        elif game.current_state.next_state == "PLAY":
            if game.current_state.return_state == "RESUME_GAME":
                game.current_state = PlayState(game)                    
            else:
                start_game()
                game.current_state = PlayState(game)                    
        elif game.current_state.next_state == "TITLE":
            if game.current_state.return_state == "RESUME_GAME":
                game.current_state = TitleState(game)
            else:
                game.current_state = TitleState(game)
        elif game.current_state.next_state == "SETTINGS":                
            if game.current_state.return_state == "PAUSE":
                game.current_state = PauseState(game)
            elif game.current_state.return_state == "TITLE":
                game.current_state = TitleState(game)                    
            else:
                game.current_state = SettingsState(game)

    # --- DRAWING SECTION ---

    screen.fill(BG_COLOUR)
    game.current_state.draw(screen)
    

    pg.display.flip()
pg.quit()
