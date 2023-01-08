import pygame
import logging

import src.utility.utility as util
from src.ui.ui import UI
from src.utility.vector import Vect

class PauseMenu(UI):
    def __init__(self, consts, uiData, bgShade):
        super().__init__(False, __name__)
        super().load(consts, "pauseMenu", uiData)

        self.backgroundShade = bgShade
    

    def update(self, window):
        """ Updates ui and tests if the player clicked off of the pause menu """
        super().update(window)

        if window.getMouseReleased("left"): # left clicked
            # test if the player clicked off of the pause menu
            mousePos = window.getMousePos()
            bg = super().getObj("bg") # pause menu background image

            # No collision between the mouse and the pause menu background
            if not util.pointRectCollision(mousePos, bg.getPos(), bg.getSize()):
                super().setDisplaying(False)
        
        
        if super().getObj("resume").getPressed(): # Resume button pressed
            super().setDisplaying(False)
    

    def render(self, window):
        """ Draws BG Shade and ui elements when displaying """
        if super().isDisplaying():
            window.render(self.backgroundShade, Vect(0, 0))

        super().render(window)
    

    def getQuitPressed(self):
        """ Quit button pressed or not """
        return super().getObj("mainMenu").getPressed()