import pygame as pg
from sprites import Explosion, Powerup, Meteoroid, Boss
from systems import game_logic
from utilities import spawn_wave
from random import random, randint
from settings import *
from typing import TYPE_CHECKING

# Use the TYPE_CHECKING guard to import for type hints only
if TYPE_CHECKING:
    from game import Game

def new_high_score_check(game: 'Game'):
    
    if game.score > game.high_score:
        game.high_score = game.score
        with open(HS_FILE, "w") as f:
            f.write(str(game.score))
        return True
    else:
        return False
    
def new_boss(game: 'Game'):
    boss = Boss(game)
    game.all_sprites_group.add(boss)
    game.bosses_group.add(boss)

def cleanup_meteoroids(game: 'Game'):
    for meteor in game.meteors_group:
        game.sound_manager.play("explosion")
        explosion = Explosion(meteor.rect.center, 'large_explosion', game.graphics_manager.explosion_animations)
        game.all_sprites_group.add(explosion)
        meteor.kill()

def new_meteroid(game: 'Game', position = None, velocity = None, is_medium = False):
    m = Meteoroid(game, position, velocity, is_medium)
    game.all_sprites_group.add(m)
    game.meteors_group.add(m)

def clear_game_objects(game: 'Game'):
    for meteoroid in game.meteors_group: 
        meteoroid.kill()
    for bullet in game.bullets_group:
        bullet.kill()
    for powerup in game.powerups_group:
        powerup.kill()

def spawn_meteoroid_wave(game: 'Game'):
    spawn_wave(new_meteroid, NUMBER_OF_METEOROIDS, game)

def handle_bullet_meteoroid_collisions(game: 'Game'):
    meteoroid_is_hit = pg.sprite.groupcollide(game.meteors_group, game.bullets_group, True, True)
    for meteor in meteoroid_is_hit:
        game.score += 62 - round(meteor.radius / game.scale_factor)
        game.sound_manager.play("explosion")
        explosion = Explosion(meteor.rect.center, 'large_explosion', game.graphics_manager.explosion_animations)
        game.all_sprites_group.add(explosion)
        if random() < POWERUP_DROP_CHANCE:
            power = Powerup(game.graphics_manager.powerup_icons, meteor.rect.center, game.screen_width, game.screen_height, game.scale_factor)
            game.all_sprites_group.add(power)
            game.powerups_group.add(power)
        if meteor.can_split():
            new_meteoroids = meteor.create_split_meteoroids()
            for new_meteor in new_meteoroids:
                game.all_sprites_group.add(new_meteor)
                game.meteors_group.add(new_meteor)
            meteor.kill()
        else:
            if len(game.meteors_group) < NUMBER_OF_METEOROIDS:
                new_meteroid(game)

def handle_player_meteoroid_collisions(game: 'Game'):
    player_is_hit = pg.sprite.spritecollide(game.player, game.meteors_group, True, pg.sprite.collide_circle)
    for meteor in player_is_hit:
        game.sound_manager.play("explosion")
        game.player.power = 1
        game.player.health -= meteor.radius * 2 / game.scale_factor
        explosion = Explosion(meteor.rect.center, 'small_explosion', game.graphics_manager.explosion_animations)
        game.all_sprites_group.add(explosion)
        new_meteroid(game)
        if game.player.health <= 0:
            game.sound_manager.play("player_die")
            clear_game_objects(game)
            game.player.lives -= 1
            # Return True to signal that the main loop should create the death explosion
            return True
    # Return False if the player didn't die in this collision
    return False


def handle_player_powerup_collisions(game: 'Game'):
    powerup_is_hit = pg.sprite.spritecollide(game.player, game.powerups_group, True)
    for power in powerup_is_hit:
        if power.type == "health_up":
            game.player.health += randint(10, 30)
            game.sound_manager.play("health_up")
            if game.player.health >= 100:
                game.player.health = 100
        if power.type == "bolt_gold":
            game.player.powerup()
            game.sound_manager.play("bolt_gold")


def handle_player_respawn(game: 'Game'):
    if game.player.just_respawned:
        if len(game.bosses_group) == 0 or game.boss_defeated:
            spawn_meteoroid_wave(game)
        game.player.rect.centerx = game.screen_width / 2
        game.player.rect.bottom = game.screen_height - PLAYER_START_Y_OFFSET
        game.player.health = 100
        game.player.just_respawned = False


def handle_bullet_boss_collisions(game: 'Game'):
    boss_hits = pg.sprite.groupcollide(game.bosses_group, game.bullets_group, False, True, pg.sprite.collide_circle)
    for boss, bullets in boss_hits.items():
        for bullet in bullets:
            game.sound_manager.play("explosion")
            explosion = Explosion(bullet.rect.midtop, 'small_explosion', game.graphics_manager.explosion_animations)
            game.all_sprites_group.add(explosion)
            boss.take_damage(2)
            if random() < 0.05:
                power = Powerup(game.graphics_manager.powerup_icons, bullet.rect.center, game.screen_width, game.screen_height, game.scale_factor)
                game.all_sprites_group.add(power)
                game.powerups_group.add(power)

            if not boss.alive:
                game.score += boss.points
                game.sound_manager.play("player_die")
                death_explosion = Explosion(boss.rect.center, 'boss_explosion', game.graphics_manager.explosion_animations)
                game.all_sprites_group.add(death_explosion)
                game.boss_defeated = True
                for bullet in game.boss_bullets_group:
                    bullet.kill()

                # Resume meteoroid spawning
                for _ in range(NUMBER_OF_METEOROIDS):
                    game_logic.new_meteroid(game)
                    
def handle_boss_bullet_player_collisions(game: 'Game'):
    """Handle boss bullets hitting player. Returns True if player died."""
    player_is_hit = pg.sprite.spritecollide(game.player, game.boss_bullets_group, True)
    for hit in player_is_hit:
        game.sound_manager.play("explosion")
        game.player.health -= 10
        explosion = Explosion(hit.rect.center, 'small_explosion', game.graphics_manager.explosion_animations)
        game.all_sprites_group.add(explosion)
        
        if game.player.health <= 0:
            game.sound_manager.play("player_die")
            clear_game_objects(game)
            game.player.lives -= 1
            return True  # Signal player death
    
    return False