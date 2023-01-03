import pygame
import logging

from src.ui.ui import UI

class DeathScreen(UI):
    def __init__(self, consts, uiData):
        super().__init__(False, __name__)

        super().load(consts, "deathScreen", uiData)
