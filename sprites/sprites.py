import pygame as pg
from random import choice
from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, bullet_image):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = BULLET_SPEED

    def update(self, dt):
        self.rect.y += self.speedy * dt
        if self.rect.bottom < 0:
            self.kill()


class Powerup(pg.sprite.Sprite):
    def __init__(self, powerup_images, center, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = choice(["shield_gold", "bolt_gold"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = POWERUP_SPEED

    def update(self, dt):
        self.rect.y += self.speedy * dt
        if self.rect.top > self.screen_height:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size, explosion_animation):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_animation = explosion_animation
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_time = 0
        self.frame_rate = EXPLOSION_FRAME_RATE

    def update(self, dt):
        self.frame_time += dt * 1000
        if self.frame_time > self.frame_rate:
            self.frame_time = 0          
            self.frame += 1
        if self.frame == len(self.explosion_animation[self.size]):
            self.kill()
        else:
            center = self.rect.center
            self.image = self.explosion_animation[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center