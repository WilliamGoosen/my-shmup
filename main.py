import pygame as pg
from settings import *
from utilities import load_config
from game import Game
from systems import game_logic
from states import PlayState, PauseState, TitleState, GameOverState, SettingsState

def _handle_state_transition(game: Game) -> None:
    """Handle transitioning between different game states."""
    next_state = game.current_state.next_state
    return_state = game.current_state.return_state
    
    state_map = {
        "GAME_OVER": GameOverState,
        "PAUSE": PauseState, 
        "PLAY": PlayState,
        "TITLE": TitleState,
        "SETTINGS": SettingsState
    }
    
    if next_state in state_map:
        if next_state == "PLAY" and return_state != "RESUME_GAME":
            game_logic.start_game(game)  # Only reset for new games, not resumes
        game.current_state = state_map[next_state](game)

def main():
    # Constants and initialisation
    config: dict = load_config()
    scale_factor = float(config.get("scale_factor", 1.0))
    screen_width = int(BASE_WIDTH * scale_factor)
    screen_height = int(BASE_HEIGHT * scale_factor)

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()

    game = Game(config, scale_factor, screen_width, screen_height)

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
            _handle_state_transition(game)

        # --- DRAWING SECTION ---
        screen.fill(BG_COLOUR)
        game.current_state.draw(screen)
        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()