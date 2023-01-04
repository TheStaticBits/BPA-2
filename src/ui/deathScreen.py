import pygame
import logging

from src.ui.ui import UI
from src.utility.vector import Vect

class DeathScreen(UI):
    def __init__(self, consts, uiData):
        super().__init__(False, __name__)

        super().load(consts, "deathScreen", uiData)

        # Make rectangle of size of the window screen
        windowSize = Vect(consts["window"]["size"]).getTuple()
        self.backgroundShade = pygame.Surface(windowSize)
        self.backgroundShade.fill((0, 0, 0)) # Fill with black
        self.backgroundShade.set_alpha(100)


    def display(self, waveNum):
        super().setDisplaying(True)
    
    
    def render(self, window):
        """ Renders background shade and the ui elements """
        if super().isDisplaying():
            window.render(self.backgroundShade, Vect(0, 0))

        super().render(window)