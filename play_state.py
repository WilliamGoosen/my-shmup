import pygame as pg
from base_state import BaseState
from game_logic import handle_bullet_meteoroid_collisions, handle_player_meteoroid_collisions, handle_player_powerup_collisions, handle_player_respawn, new_high_score_check
from sprites import Explosion

class PlayState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        print("Playstate initialised")

    def startup(self):
        print("Playstate is starting up")

    def get_event(self, event):
        print(f"Playstate received event: {event}")
        if event.type == pg.KEYDOWN:
             if event.key == pg.K_ESCAPE:
                  self.done = True
                  self.next_state = "PAUSE"

    def update(self, dt):
        
        handle_player_respawn(
            self.game.player,
            self.game.graphics_manager,
            self.game.WIDTH,
            self.game.HEIGHT,
            self.game.all_sprites_group,
            self.game.meteors_group
        )
            
        # check to see if a bullet hit a meteoroid
        self.game.score = handle_bullet_meteoroid_collisions(
            self.game.meteors_group,
            self.game.bullets_group,
            self.game.score,
            self.game.sound_manager,
            self.game.graphics_manager,
            self.game.all_sprites_group,
            self.game.powerups_group,
            self.game.WIDTH,
            self.game.HEIGHT
        )

        # check to see if a meteoroid hits the player
        player_died = handle_player_meteoroid_collisions(
            self.game.player,
            self.game.meteors_group,
            self.game.bullets_group,
            self.game.powerups_group,
            self.game.all_sprites_group,
            self.game.sound_manager,
            self.game.graphics_manager,
            self.game.WIDTH,
            self.game.HEIGHT
            )
        
        # If the function says the player died, THEN we create the explosion here in main.py.
        if player_died:
            death_explosion = Explosion(
                self.game.player.rect.center,
                'player_explosion',
                self.game.graphics_manager.explosion_animations)
            self.game.all_sprites_group.add(death_explosion)
            self.game.player.hide()

        # check to see if player hit a powerup
        handle_player_powerup_collisions(
            self.game.player,
            self.game.powerups_group,
            self.game.sound_manager) 

        if self.game.player.lives == 0 and death_explosion and not death_explosion.alive():
                self.done = True
                self.next_state = "GAME_OVER"
                self.game.new_high_score_achieved = new_high_score_check(self.game)       

    def draw(self, surface):
        surface.fill((30, 30, 60))
