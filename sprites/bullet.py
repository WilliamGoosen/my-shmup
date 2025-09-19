import pygame as pg
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