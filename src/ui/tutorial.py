import pygame
import logging

from src.ui.ui import UI

class Tutorial(UI):
    """ Handles tutorial ui """

    def __init__(self, consts, uiData):
        super().__init__(False, __name__)
        
        super().load(consts, "tutorial", uiData)
    

    def update(self, window):
        """ Updates left/right buttons"""
        super().update(window)