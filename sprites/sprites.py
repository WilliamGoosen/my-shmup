import pygame as pg
from random import randrange, uniform, choice, randint
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


class Meteoroid(pg.sprite.Sprite):
    def __init__(self, meteor_images, screen_width, screen_height, 
                 position=None, velocity=None, is_medium=False):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.meteor_images = meteor_images
        self.is_medium = is_medium
        self.pos = pg.math.Vector2(0, 0) # Float position tracking
        
        # Initialize state
        self.initialize_meteoroid(position, velocity)

    def update(self, dt):
        self.rotate(dt)
        self.pos.x += self.speedx * dt
        self.pos.y += self.speedy * dt
        
        # Update integer rect for drawing/collision
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if self.is_off_screen():
            self.initialize_meteoroid()  # Full reset

    def initialize_meteoroid(self, position=None, velocity=None):
        """Initialize or reset meteoroid with optional position/velocity"""
        self.image_orig = choice(self.meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)

        # Set position
        if position:
            self.rect.centerx, self.rect.bottom = position
        else:
            self.rect.centerx = randrange(self.screen_width - self.rect.width)
            self.rect.bottom = randrange(-METEOROID_SPAWN_Y_MAX, -METEOROID_SPAWN_Y_MIN)
        
        self.pos.x = self.rect.centerx
        self.pos.y = self.rect.centery

        # Set velocity
        if velocity:
            self.speedx, self.speedy = velocity
        else:
            self.speedx = randint(METEOROID_MIN_SPEED_X, METEOROID_MAX_SPEED_X)
            self.speedy = randint(METEOROID_MIN_SPEED_Y, METEOROID_MAX_SPEED_Y)

        # Rotation
        self.rot = 0
        self.frame_time = 0
        self.rot_speed = randint(METEOROID_MIN_ROTATE_SPEED, METEOROID_MAX_ROTATE_SPEED)

    def can_split(self):
        return self.radius > 40  # Extract constant

    def create_split_meteoroids(self, meteor_images_medium):
        """Return new meteoroids from split, without adding to groups"""
        left_pos = (self.rect.centerx, self.rect.centery)
        right_pos = (self.rect.centerx, self.rect.centery)
        
        left_velocity = (self.speedx - METEOROID_SPLIT_SPEED_BOOST, self.speedy)
        right_velocity = (self.speedx + METEOROID_SPLIT_SPEED_BOOST, self.speedy)

        return [
            Meteoroid(meteor_images_medium, self.screen_width, self.screen_height,
                     position=left_pos, velocity=left_velocity, is_medium=True),
            Meteoroid(meteor_images_medium, self.screen_width, self.screen_height,
                     position=right_pos, velocity=right_velocity, is_medium=True)
        ]

    def rotate(self, dt):
            self.rot = (self.rot + self.rot_speed * dt) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot).convert_alpha()
            current_pos = self.pos.copy()
            self.image = new_image
            self.rect = self.image.get_rect()
            self.pos = current_pos
            self.rect.center = (int(self.pos.x), int(self.pos.y))

    def is_off_screen(self):
        return (self.rect.top > self.screen_height + self.rect.height or 
                self.rect.left < -self.rect.width or 
                self.rect.right > self.screen_width + self.rect.width)


class Starfield(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = randint(1, STAR_MAX_RADIUS)
        self.pos_y = uniform(0, screen_height)
        self.speedy = uniform(STAR_MIN_SPEED, STAR_MAX_SPEED + 1)
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

    def update(self, dt):
        self.pos_y += self.speedy * dt
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