import pygame as pg
import math
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - PLAYER_START_Y_OFFSET
        self.speedx = 0
        self.speedy = 0


    def update(self, keystate):
        self.speedx = 0
        if keystate[pg.K_LEFT] and not keystate[pg.K_RIGHT]:
            self.speedx = -PLAYER_SPEED
        elif keystate[pg.K_RIGHT] and not keystate[pg.K_LEFT]:
            self.speedx = PLAYER_SPEED
        else:
            self.speedx = 0
        
        self.speedy = 0
        if keystate[pg.K_UP] and not keystate[pg.K_DOWN]:
            self.speedy = -PLAYER_SPEED
        elif keystate[pg.K_DOWN] and not keystate[pg.K_UP]:
            self.speedy = PLAYER_SPEED
        else:
            self.speedy = 0

        if self.speedx != 0 and self.speedy != 0:
            self.speedx = self.speedx / math.sqrt(2)
            self.speedy = self.speedy / math.sqrt(2)   
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
