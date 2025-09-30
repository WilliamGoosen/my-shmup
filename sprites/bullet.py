import pygame as pg
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, scale_factor: float, bullet_image: pg.Surface, speed_direction: int) -> None:
        pg.sprite.Sprite.__init__(self)
        self.scale_factor = scale_factor
        self.image = bullet_image
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.centerx = x
        self.speedy = BULLET_SPEED * scale_factor * speed_direction
        
        # Position based on direction
        if speed_direction > 0: # Downward bullets (enemy): start at top of sprite
            self.rect.bottom = y
        else: # Upward bullets (player): start at bottom of sprite  
            self.rect.top = y

    def update(self, dt):
        self.rect.y += self.speedy * dt
        if self.rect.bottom < 0 or self.rect.top > BASE_HEIGHT * self.scale_factor:
            self.kill()
            
            
class PlayerBullet(Bullet):
    def __init__(self, x: int, y: int, scale_factor: float, bullet_image: pg.Surface):
        super().__init__(x, y, scale_factor, bullet_image, speed_direction = -1)
        
class BossBullet(Bullet):
    def __init__(self, x, y, scale_factor, bullet_image):
        super().__init__(x, y, scale_factor, bullet_image, speed_direction = 1)