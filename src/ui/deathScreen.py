import pygame
import logging

from src.ui.ui import UI
from src.utility.vector import Vect

class DeathScreen(UI):
    """ Handles the simple ui that pops up upon the player losing all health and dying. """

    def __init__(self, consts, uiData, bgShade):
        super().__init__(False, __name__)

        super().load(consts, "deathScreen", uiData)

        self.backgroundShade = bgShade


    def showDeath(self, prevHighscore, waveNum):
        self.log.info(f"Showing death screen of wave {waveNum} with previous highscore of {prevHighscore}.")

        super().setDisplaying(True)
        
        message = f"You got to wave {waveNum}!\n"

        if waveNum > prevHighscore:
            message += f"You beat your previous\nhighscore of wave {prevHighscore}!"
        else:
            message += f"You didn't beat your previous\nhighscore of wave {prevHighscore}."
        
        super().getObj("waveNum").setText(message)
    
    
    def render(self, window):
        """ Renders background shade and the ui elements """
        if super().isDisplaying():
            window.render(self.backgroundShade, Vect(0, 0))

        super().render(window)
    
    
    def pressedContinue(self):
        return super().getObj("continue").getPressed()