import pygame as pg
from settings import *
from utilities import load_config
from game import Game
from systems import game_logic
from states import PlayState, PauseState, TitleState, GameOverState, SettingsState

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

            if game.current_state.next_state == "GAME_OVER":
                game.current_state = GameOverState(game)
            elif game.current_state.next_state == "PAUSE":
                game.current_state = PauseState(game)
            elif game.current_state.next_state == "PLAY":
                if game.current_state.return_state == "RESUME_GAME":
                    game.current_state = PlayState(game)
                else:
                    game_logic.start_game(game)
                    game.current_state = PlayState(game)
            elif game.current_state.next_state == "TITLE":
                game.current_state = TitleState(game)
            elif game.current_state.next_state == "SETTINGS":
                game.current_state = SettingsState(game)

        # --- DRAWING SECTION ---

        screen.fill(BG_COLOUR)
        game.current_state.draw(screen)


        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()
