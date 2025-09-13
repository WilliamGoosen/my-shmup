import pygame as pg
from base_state import BaseState

class PlayState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        print("Playstate initialised")

    def startup(self):
        print("Playstate is starting up")

    def get_event(self, event):
        print(f"Playstate received event: {event}")

    def update(self, dt):
        print(f"Playstate updating. DT: {dt}")

    def draw(self, surface):
        surface.fill((30, 30, 60))
