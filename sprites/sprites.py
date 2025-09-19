import pygame as pg
from settings import *


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