import pygame as pg
import math
from random import random, randrange, uniform, choice, randint
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, all_sprite_group, bullets_group, shoot_sound, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load('img/playerShip1_orange.png'), (50, 38)) #pg.Surface((50, 40))
        self.image.set_colorkey(BLACK) #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - PLAYER_START_Y_OFFSET
        self.speedx = 0
        self.speedy = 0
        self.shield = PLAYER_MAX_SHIELD
        self.shoot_sound = shoot_sound
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.last_shot = pg.time.get_ticks()
        self.lives = PLAYER_START_LIVES
        self.hidden = False
        self.all_sprites = all_sprite_group
        self.bullets = bullets_group
        self.power = PLAYER_START_POWER
        self.just_respawned = False
        self.power_time = pg.time.get_ticks()


    def update(self):
        if not self.hidden:
            if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
                self.power -= 1
                self.power_time = pg.time.get_ticks()        

            if self.speedx != 0 and self.speedy != 0:
                self.speedx = self.speedx / math.sqrt(2)
                self.speedy = self.speedy / math.sqrt(2)   

            self.rect.x += self.speedx
            self.rect.y += self.speedy

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

    def update_with_keystate(self, keystate, sound_enabled):
        if self.hidden:
            return
                    
        if keystate[pg.K_SPACE]:            
            self.shoot(sound_enabled)

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

    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()


    def shoot(self, sound_enabled):
        if not self.hidden:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:            
                self.last_shot = now
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
                    bullet = Bullet(bullet_location[0], bullet_location[1])
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                if sound_enabled:
                    self.shoot_sound.play()                


    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (self.screen_width / 2, self.screen_height + self.rect.height / 2)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('img/laserRed16.png')
        self.image.set_colorkey(BLACK)    #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Meteoroid(pg.sprite.Sprite):
    def __init__(self, meteor_images, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.meteor_images = meteor_images
        self.last_update = pg.time.get_ticks()
        self.reset()
    
    def reset(self):
        self.image_orig = choice(self.meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = randrange(self.screen_width - self.rect.width)
        self.rect.y = randrange(-150, -100)
        self.speedx = randint(METEOROID_MIN_SPEED_X, METEOROID_MAX_SPEED_X)
        self.speedy = randint(METEOROID_MIN_SPEED_Y, METEOROID_MAX_SPEED_Y)
        self.rot = 0
        self.rot_speed = randint(METEOROID_MIN_ROTATE_SPEED, METEOROID_MAX_ROTATE_SPEED)
    
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot).convert_alpha()
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.screen_height + self.rect.height or self.rect.left < -self.rect.width or self.rect.right > self.screen_width + self.rect.width:
            self.reset()
            # self.rect.x = randrange(WIDTH - self.rect.width)
            # self.rect.y = randrange(-100, -40)
            # self.speedy = randint(METEOROID_MIN_SPEED_Y, METEOROID_MAX_SPEED_Y)
        

class Starfield(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = randint(1, STAR_MAX_RADIUS)
        self.pos_y = uniform(0, screen_height)
        self.speedy = uniform(0.1, STAR_MAX_SPEED + 1)
                
        shapes = ['pixel', 'square', 'circle']
        shape = choice(shapes)
        
        if shape == 'pixel':
            self.image = pg.Surface((1, 1), pg.SRCALPHA)
            self.image.set_at((0, 0), WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = randint(0, self.screen_width - self.rect.width)
            
        elif shape == 'square':
            self.image = pg.Surface((2, 2), pg.SRCALPHA)
            pg.draw.rect(self.image, WHITE, self.image.get_rect())
            self.rect = self.image.get_rect()
            self.rect.x = randint(0, self.screen_width - self.rect.width)
            
        elif shape == 'circle':
            self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
            pg.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)
            self.rect = self.image.get_rect()
            self.rect.x = randint(0, self.screen_width - self.rect.width)
        
    def update(self):
        self.pos_y += self.speedy
        self.rect.y = int(self.pos_y)
        if self.rect.top > self.screen_height:
            self.pos_y = -self.rect.height
            self.rect.y = int(self.pos_y)
            self.rect.x = randint(0, self.screen_width - self.rect.width)

class Powerup(pg.sprite.Sprite):
    def __init__(self, powerup_images, center, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = POWERUP_SPEED
    
    def update(self):
        self.rect.y += self.speedy
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
        self.last_update = pg.time.get_ticks()
        self.frame_rate = EXPLOSION_FRAME_RATE
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
        if self.frame == len(self.explosion_animation[self.size]):
            self.kill()
        else:
            center = self.rect.center
            self.image = self.explosion_animation[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center