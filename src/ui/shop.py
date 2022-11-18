import pygame
import logging

from src.ui.ui import UI
from src.ui.button import Button

class Shop(UI):
    def __init__(self, uiData):
        super().__init__(True)

        super().load("shop", uiData)

        