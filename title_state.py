import pygame as pg
from base_state import BaseState

class TitleState(BaseState):
    def __init__(self, game):
        super().__init__(game)

    def startup(self):
        super().startup()

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass