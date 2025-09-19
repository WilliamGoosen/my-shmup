import pygame as pg
from random import choice
from settings import *

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
