import pygame as pg
from sprites import BossBullet
from settings import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

class Enemy(pg.sprite.Sprite):
    """Base class for all enemies"""
    def __init__(self, game: 'Game', health: int, points: int):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.health = health
        self.max_health = health
        self.points = points
        self.alive: bool = True
        
    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            self.die()
            
    def die(self):
        self.alive = False
        self.kill()


class Boss(Enemy):
    def __init__(self, game: 'Game'):
        super().__init__(game, health = 100, points= 5000)
        self.game = game
        self.scale_factor = game.scale_factor
        self.screen_width = game.screen_width
        self.screen_height = game.screen_height
        self.image_orig = game.graphics_manager.boss_image
        self.image = self.image_orig.copy()
        self.rect: pg.Rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.5)
        self.last_update = pg.time.get_ticks()
        
        # Initial position
        self.rect.midbottom = (self.screen_width * 0.5, -self.rect.height)
        self.pos = pg.math.Vector2(self.rect.centerx, self.rect.centery)
        self.rot = 0
        
        # Movement variables
        self.speedx = 0
        self.speedy = 0
        self.rot_speed = 30
        
        # Shooting variables
        self.shoot_delay = 750
        self.bullet_frame_time: float = 0
        self.bullet_image: pg.Surface = game.graphics_manager.boss_bullet_image
        # self.last_shot = pg.time.get_ticks()
        
    def update(self, dt):
        self.rotate()

        # Movement logic from your original code
        if self.game.score > BOSS_SPAWN_SCORE:
            self.speedy = 180 * self.scale_factor

        self.pos.x += self.speedx * dt
        self.pos.y += self.speedy * dt

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

        # Stop at top of screen
        if self.rect.bottom > int(self.rect.height / 2):
            self.rect.bottom = int(self.rect.height / 2)
            self.speedy = 0

        # Start side-to-side movement and shooting once positioned
        if self.speedy == 0 and self.rect.bottom == int(self.rect.height / 2):
            
            self.shoot(dt)
            if self.speedx == 0:
                self.speedx = 120 * self.scale_factor
                
        # Bounce off screen edges
        if self.pos.x + self.radius > self.screen_width:
            # self.rect.right = self.screen_width
            self.speedx = -self.speedx
        if self.pos.x - self.radius < 0:
            # self.rect.left = 0
            self.speedx = -self.speedx

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 500:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def shoot(self, dt):
        self.bullet_frame_time += dt * 1000
        if self.bullet_frame_time > self.shoot_delay:
            self.bullet_frame_time = 0
            bullet_locations = [
                (self.rect.centerx, self.rect.bottom - 0.4 * self.radius),
                (self.rect.centerx - 0.7 * self.radius, self.rect.bottom - 0.7 * self.radius),
                (self.rect.centerx + 0.7 * self.radius, self.rect.bottom - 0.7 * self.radius)
                ]
            for bullet_location in bullet_locations:
                bullet = BossBullet(bullet_location[0], bullet_location[1], self.scale_factor, self.bullet_image)
                self.game.all_sprites_group.add(bullet)
                self.game.boss_bullets_group.add(bullet)
            self.game.sound_manager.play("shoot")