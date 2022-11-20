import pygame
import logging

from src.ui.ui import UI
from src.ui.button import Button

class Shop(UI):
    def __init__(self, consts, uiData):
        super().__init__(True)

        super().load(consts, "shop", uiData)
    

    def update(self, window):
        """ Handles button events and shop-related updates """
        super().update(window)

    
    def render(self, window):
        """ Handles shop-specific rendering events """
        super().render(window)