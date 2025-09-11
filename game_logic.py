import pygame as pg
from sprites import Explosion, Powerup, Meteoroid
from random import random
from settings import *

def new_meteroid(meteor_images, width, height, all_sprites_group, meteors_group, position = None, velocity = None, is_medium = False):
    m = Meteoroid(meteor_images, width, height, position, velocity, is_medium)
    all_sprites_group.add(m)
    meteors_group.add(m)

def clear_game_objects(meteors_group, bullets_group, powerups_group):
    for meteoroid in meteors_group: 
        meteoroid.kill()
    for bullet in bullets_group:
        bullet.kill()
    for powerup in powerups_group:
        powerup.kill()

def handle_bullet_meteoroid_collisions(meteors_group, bullets_group, current_score, sound_mgr,
                                       graphics_mgr, all_sprites_group, powerups_group, width, height):
    meteoroid_is_hit = pg.sprite.groupcollide(meteors_group, bullets_group, True, True)
    for meteor in meteoroid_is_hit:
        current_score += 62 - meteor.radius
        sound_mgr.play("explosion")
        explosion = Explosion(meteor.rect.center, 'large_explosion', graphics_mgr.explosion_animations)
        all_sprites_group.add(explosion)
        if random() < POWERUP_DROP_CHANCE:
            power = Powerup(graphics_mgr.powerup_icons, meteor.rect.center, width, height)
            all_sprites_group.add(power)
            powerups_group.add(power)
        if meteor.can_split():
            new_meteoroids = meteor.create_split_meteoroids(graphics_mgr.meteoroid_images_medium)
            for new_meteor in new_meteoroids:
                all_sprites_group.add(new_meteor)
                meteors_group.add(new_meteor)
            meteor.kill()
        else:
            if len(meteors_group) < NUMBER_OF_METEOROIDS:
                new_meteroid(graphics_mgr.meteoroid_images, width, height, all_sprites_group, meteors_group)
    return current_score

def handle_player_meteoroid_collisions(player, meteors_group, bullets_group, powerups_group, all_sprites_group, sound_mgr, graphics_mgr, width, height):
    player_is_hit = pg.sprite.spritecollide(player, meteors_group, True, pg.sprite.collide_circle)    
    for meteor in player_is_hit:
        sound_mgr.play("explosion")
        player.power = 1
        player.shield -= meteor.radius * 2
        explosion = Explosion(meteor.rect.center, 'small_explosion', graphics_mgr.explosion_animations)
        all_sprites_group.add(explosion)
        new_meteroid(graphics_mgr.meteoroid_images, width, height, all_sprites_group, meteors_group)        
        if player.shield <= 0:
            sound_mgr.play("player_die")            
            clear_game_objects(meteors_group, bullets_group, powerups_group)
            player.lives -= 1
            player.shield = 100
            # Return True to signal that the main loop should create the death explosion
            return True
        
    # Return False if the player didn't die in this collision
    return False
    