import pygame
import logging

from src.ui.ui import UI

class Error(UI):
    """ Displays error message and gives the user options for how to handle the error """

    def __init__(self, consts, uiData):
        super().__init__(self, __name__)

        super().load(consts, "error", uiData)


    def update(self, window):
        """ Handles error button presses """
        super().update(window)