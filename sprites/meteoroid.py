import pygame as pg
from random import randrange, randint, choice
from settings import *

class Meteoroid(pg.sprite.Sprite):
    def __init__(self, meteor_images, screen_width, screen_height, scale_factor: float,
                 position=None, velocity=None, is_medium=False):
        pg.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_factor = scale_factor
        self.meteor_images = meteor_images
        self.is_medium = is_medium
        self.rect: pg.Rect
        self.pos = pg.math.Vector2(0, 0) # Float position tracking
        
        # Initialize state
        self.initialize_meteoroid(position, velocity)

    def update(self, dt):
        self.rotate(dt)
        self.pos.x += self.speedx * dt
        self.pos.y += self.speedy * dt
        
        # Update integer rect for drawing/collision
        self.rect.center = (round(self.pos.x), round(self.pos.y))

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
            self.speedx = randint(METEOROID_MIN_SPEED_X, METEOROID_MAX_SPEED_X) * self.scale_factor
            self.speedy = randint(METEOROID_MIN_SPEED_Y, METEOROID_MAX_SPEED_Y) * self.scale_factor

        # Rotation
        self.rot = 0
        self.frame_time = 0
        self.rot_speed = randint(METEOROID_MIN_ROTATE_SPEED, METEOROID_MAX_ROTATE_SPEED)

    def can_split(self):
        return self.radius > 40 * self.scale_factor  # Extract constant

    def create_split_meteoroids(self, meteor_images_medium):
        """Return new meteoroids from split, without adding to groups"""
        left_pos = (self.rect.centerx, self.rect.centery)
        right_pos = (self.rect.centerx, self.rect.centery)
        
        left_velocity = (self.speedx - METEOROID_SPLIT_SPEED_BOOST * self.scale_factor, self.speedy)
        right_velocity = (self.speedx + METEOROID_SPLIT_SPEED_BOOST * self.scale_factor, self.speedy)

        return [
            Meteoroid(meteor_images_medium, self.screen_width, self.screen_height, self.scale_factor,
                     position=left_pos, velocity=left_velocity, is_medium=True),
            Meteoroid(meteor_images_medium, self.screen_width, self.screen_height, self.scale_factor,
                     position=right_pos, velocity=right_velocity, is_medium=True)
        ]

    def rotate(self, dt):
            self.rot = (self.rot + self.rot_speed * dt) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot).convert_alpha()
            current_pos = self.pos.copy()
            self.image = new_image
            self.rect = self.image.get_rect()
            self.pos = current_pos
            self.rect.center = (round(self.pos.x), round(self.pos.y))

    def is_off_screen(self):
        return (self.rect.top > self.screen_height + self.rect.height or 
                self.rect.left < -self.rect.width or 
                self.rect.right > self.screen_width + self.rect.width)