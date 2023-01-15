import pygame
import logging

from src.ui.error import Error
from src.ui.ui import UI
from src.utility.vector import Vect

class Warning(UI):
    """ Handles the warning screen that pops up when the player reaches wave 65 """
    def __init__(self, consts, uiData, bgShade):
        super().__init__(False, __name__)
        super().load(consts, "warning", uiData)
        self.backgroundShade = bgShade

        try:
            self.warningWave = consts["game"]["warningWave"]
        except KeyError as exc:
            Error.createError("Unable to find warning wave num in constants.json.", self.log, exc)

    
    def update(self, window):
        super().update(window)

        # Testing if continue button pressed
        if super().getObj("continue").getPressed():
            super().setDisplaying(False)
        

    def detect(self, wavesObj):
        """ Detects when to display the warning"""
        if wavesObj.getChangedWave(): # Frame on which the wave num changed
            # If wave number is the warning wave, set the warning to true
            if (wavesObj.getWaveNum() + 1) == self.warningWave:
                super().setDisplaying(True)

    
    def render(self, window):
        """ Renders background shade and the ui elements """
        if super().isDisplaying():
            window.render(self.backgroundShade, Vect(0, 0))

        super().render(window)