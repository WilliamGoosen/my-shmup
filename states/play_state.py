import pygame as pg
from states.base_state import BaseState
from systems import game_logic
from sprites import Explosion
from utilities import draw_lives, draw_health_bar, draw_text
from settings import *
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game

class PlayState(BaseState):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.death_explosion = None
        self.game: Game = game

    def startup(self):
        super().startup()
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
             if event.key == pg.K_ESCAPE:
                  self.done = True
                  self.next_state = "PAUSE"

    def update(self, dt):
        self.game.all_sprites_group.update(dt)

        game_logic.handle_player_respawn(
            self.game.player,
            self.game.graphics_manager,
            self.game.screen_width,
            self.game.screen_height,
            self.game.all_sprites_group,
            self.game.meteors_group,
            self.game.scale_factor
        )
            
        # check to see if a bullet hit a meteoroid
        self.game.score = game_logic.handle_bullet_meteoroid_collisions(
            self.game.meteors_group,
            self.game.bullets_group,
            self.game.score,
            self.game.sound_manager,
            self.game.graphics_manager,
            self.game.all_sprites_group,
            self.game.powerups_group,
            self.game.screen_width,
            self.game.screen_height,
            self.game.scale_factor
        )

        # check to see if a meteoroid hits the player
        player_died = game_logic.handle_player_meteoroid_collisions(
            self.game.player,
            self.game.meteors_group,
            self.game.bullets_group,
            self.game.powerups_group,
            self.game.all_sprites_group,
            self.game.sound_manager,
            self.game.graphics_manager,
            self.game.screen_width,
            self.game.screen_height,
            self.game.scale_factor
            )
        
        if len(self.game.bosses_group) == 0 and self.game.score > BOSS_SPAWN_SCORE:
            game_logic.new_boss(self.game)
        
        # If the function says the player died, THEN we create the explosion here in main.py.
        if player_died:
            self.death_explosion = Explosion(
                self.game.player.rect.center,
                'player_explosion',
                self.game.graphics_manager.explosion_animations)
            self.game.all_sprites_group.add(self.death_explosion)
            self.game.player.hide()

        # check to see if player hit a powerup
        game_logic.handle_player_powerup_collisions(
            self.game.player,
            self.game.powerups_group,
            self.game.sound_manager) 

        if self.game.player.lives == 0 and self.death_explosion and not self.death_explosion.alive():
                self.done = True
                self.next_state = "GAME_OVER"
                self.game.new_high_score_achieved = game_logic.new_high_score_check(self.game)        

    def draw(self, surface):
        scale_factor = self.game.scale_factor
        self.game.all_sprites_group.draw(surface)
        
        draw_text(
             surface,
             "Score: " + str(self.game.score),
             round(22 * scale_factor),
             self.game.screen_width / 2,
             self.game.screen_height * 0.01,
             self.game.font_name,
             WHITE
        )
        draw_lives(
             surface,
             self.game,
             self.game.player.lives,
             self.game.graphics_manager.player_icon
        )
        draw_health_bar(
             surface,
             self.game,
             self.game.player.shield
        )