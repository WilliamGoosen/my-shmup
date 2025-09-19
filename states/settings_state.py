import pygame as pg
from states.base_state import BaseState

class SettingsState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        
    def startup(self):
        return super().startup()
    
    def get_event(self, event):
        return super().get_event(event)
    
    def update(self, dt):
        return super().update(dt)
    
    def draw(self, surface):
        return super().draw(surface)