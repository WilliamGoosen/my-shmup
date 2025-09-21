import pygame as pg
from os import path
from random import choice
from settings import *

class SoundManager:
    def __init__(self, music_volume, sound_volume):
        self.sounds = {} # Holds the pg.mixer.Sound objects
        self.volumes = {} # Remembers the original volume for each sound
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self.current_track = None
        self.music_enabled = True
        self.sound_enabled = True
        self.play_music("gameplay")
        for sound_name, sound_data in SOUND_CONFIG.items():
            filename, base_volume = sound_data
            self.load_sound(sound_name, filename, base_volume)

    def load_sound(self, name, files, volume):
        if isinstance(files, list):
            sound_list = []
            for file in files:
                sound = pg.mixer.Sound(path.join("snd", file))
                sound_list.append(sound)
            self.sounds[name] = sound_list
            self.volumes[name] = volume
            self.update_sound_volume(name)
        else:
            sound = pg.mixer.Sound(path.join("snd", files))
            self.sounds[name] = sound
            self.volumes[name] = volume
            self.update_sound_volume(name)

    def update_sound_volume(self, name):
        final_volume = self.volumes[name] * self.sound_volume * self.sound_enabled
        sound_obj = self.sounds[name]
        if isinstance(sound_obj, list):
            for sound in sound_obj:
                sound.set_volume(final_volume)
        else:
            sound_obj.set_volume(final_volume)

    def update_music_volume(self):
        if self.current_track:
            track_data = MUSIC_CONFIG[self.current_track]
            base_volume = track_data["volume"]
            final_volume = base_volume * self.music_volume
            pg.mixer.music.set_volume(final_volume)

    def set_sound_volume(self, level):
        self.sound_volume = level
        for name in self.sounds:
            self.update_sound_volume(name)

    def set_music_volume(self, level):
        self.music_volume = level
        self.update_music_volume()

    def play(self, name):
        sound_obj = self.sounds[name]
        if isinstance(sound_obj, list):
            sound = choice(sound_obj)
            sound.play()
        else:
            sound_obj.play()

    def play_music(self, track_name):
        self.current_track = track_name
        track_data = MUSIC_CONFIG[track_name]
        pg.mixer.music.load(path.join("snd", track_data["file"]))
        pg.mixer.music.set_volume(track_data["volume"] * self.music_volume)
        pg.mixer.music.play(loops = track_data["loops"])

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()
        return self.music_enabled
    
    def toggle_sound(self):        
        self.sound_enabled = not self.sound_enabled           
        self.set_sound_volume(self.sound_volume)
        


