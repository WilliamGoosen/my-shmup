import pygame as pg
from random import uniform, randint, choice
from settings import *

class Starfield(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height, scale_factor: float):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = randint(1, STAR_MAX_RADIUS)
        self.scale_factor = scale_factor
        self.pos_y = uniform(0, screen_height)
        self.speedy = uniform(STAR_MIN_SPEED, STAR_MAX_SPEED + 1) * self.scale_factor
        shapes = ['pixel', 'square', 'circle']
        shape = choice(shapes)

        if shape == 'pixel':
            self.image = pg.Surface((1, 1), pg.SRCALPHA)
            self.image.set_at((0, 0), WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = randint(0, self.screen_width - self.rect.width)
        elif shape == 'square':
            scaled_size = max(1, int(2 * self.scale_factor))
            self.image = pg.Surface((scaled_size, scaled_size), pg.SRCALPHA)
            pg.draw.rect(self.image, WHITE, self.image.get_rect())
            self.rect = self.image.get_rect()
            self.rect.x = randint(0, self.screen_width - self.rect.width)
        elif shape == 'circle':
            scaled_radius = max(1, int(self.radius * self.scale_factor ))
            self.image = pg.Surface((scaled_radius * 2, scaled_radius * 2), pg.SRCALPHA)
            pg.draw.circle(self.image, WHITE, (scaled_radius, scaled_radius), scaled_radius)
            self.rect = self.image.get_rect()
            self.rect.x = randint(0, self.screen_width - self.rect.width)

    def update(self, dt):
        self.pos_y += self.speedy * dt
        self.rect.y = int(self.pos_y)
        if self.rect.top > self.screen_height:
            self.pos_y = -self.rect.height
            self.rect.y = int(self.pos_y)
            self.rect.x = randint(0, self.screen_width - self.rect.width)