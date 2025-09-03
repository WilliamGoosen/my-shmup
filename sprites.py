import pygame as pg
import math
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, all_sprite_group, bullets_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - PLAYER_START_Y_OFFSET
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.last_shot = pg.time.get_ticks()
        self.all_sprites = all_sprite_group
        self.bullets = bullets_group
        self.power = PLAYER_START_POWER
        self.power_time = pg.time.get_ticks()


    def update(self, keystate):

        if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()

        if keystate[pg.K_SPACE]:
            self.shoot()

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

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:            
            self.last_shot = now
            if self.power == 1:                
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)



class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
