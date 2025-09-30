import pygame as pg
import math
from sprites import PlayerBullet
from settings import *
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game

class Player(pg.sprite.Sprite):
    def __init__(self, game: 'Game'):
        pg.sprite.Sprite.__init__(self)
        self.image = game.graphics_manager.player_image
        self.image.set_colorkey(BLACK)
        self.rect: pg.Rect = self.image.get_rect()
        self.bullet_image: pg.Surface = game.graphics_manager.bullet_image
        self.scale_factor: float = game.scale_factor
        self.screen_width = game.screen_width
        self.screen_height = game.screen_height
        self.rect.centerx = game.screen_width / 2
        self.rect.bottom = game.screen_height - PLAYER_START_Y_OFFSET
        self.speedx = 0
        self.speedy = 0
        self.health = PLAYER_MAX_HEALTH
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.bullet_frame_time = 0
        self.space_was_pressed = False
        self.lives: int = PLAYER_START_LIVES
        self.hidden = False
        self.all_sprites = game.all_sprites_group
        self.bullets = game.bullets_group
        self.power = PLAYER_START_POWER
        self.just_respawned = False
        self.input_cooldown_timer = 0.3
        self.power_time = pg.time.get_ticks()
        self.sound_manager = game.sound_manager

    def update(self, dt):
        if self.input_cooldown_timer > 0:
            self.input_cooldown_timer -= dt
            return
        if not self.hidden:
            keystate= pg.key.get_pressed()
            if keystate[pg.K_SPACE]:
                if not self.space_was_pressed:
                    self.bullet_frame_time = self.shoot_delay
                    self.space_was_pressed = True
                self.shoot(self.sound_manager, dt)
            else:
                self.space_was_pressed = False

            self.speedx = 0
            if keystate[pg.K_LEFT] and not keystate[pg.K_RIGHT]:
                self.speedx = -PLAYER_SPEED * self.scale_factor
            elif keystate[pg.K_RIGHT] and not keystate[pg.K_LEFT]:
                self.speedx = PLAYER_SPEED * self.scale_factor
            else:
                self.speedx = 0

            self.speedy = 0
            if keystate[pg.K_UP] and not keystate[pg.K_DOWN]:
                self.speedy = -PLAYER_SPEED * self.scale_factor
            elif keystate[pg.K_DOWN] and not keystate[pg.K_UP]:
                self.speedy = PLAYER_SPEED * self.scale_factor
            else:
                self.speedy = 0
            
            if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
                self.power -= 1
                self.power_time = pg.time.get_ticks()

            if self.speedx != 0 and self.speedy != 0:
                self.speedx = self.speedx / math.sqrt(2)
                self.speedy = self.speedy / math.sqrt(2)

            self.rect.x += self.speedx * dt
            self.rect.y += self.speedy * dt

            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width
            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.bottom > self.screen_height:
                self.rect.bottom = self.screen_height
            if self.rect.top < 0:
                self.rect.top = 0

        # unhide if hidden
        else:
            if (pg.time.get_ticks() - self.hide_timer) > PLAYER_RESPAWN_TIME:
                self.hidden = False
                self.just_respawned = True

    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def shoot(self, sound_manager, dt):
        if not self.hidden:
            self.bullet_frame_time += dt * 1000
            if self.bullet_frame_time > self.shoot_delay:
                self.bullet_frame_time = 0
                bullet_locations = []
                if self.power == 1:
                    bullet_locations = [(self.rect.centerx, self.rect.top)]
                elif self.power == 2:
                    bullet_locations = [(self.rect.left, self.rect.centery),
                                        (self.rect.right, self.rect.centery)]
                else:
                    bullet_locations = [(self.rect.centerx, self.rect.top),
                                    (self.rect.left, self.rect.centery),
                                    (self.rect.right, self.rect.centery)]
                for bullet_location in bullet_locations:
                    bullet = PlayerBullet(bullet_location[0], bullet_location[1], self.scale_factor, self.bullet_image)
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                sound_manager.play("shoot")

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (self.screen_width / 2, self.screen_height + 2 * self.rect.height)

