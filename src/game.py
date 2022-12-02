import pygame
import logging

import src.utility.utility as util
from src.window import Window
from src.round import Round
from src.ui.error import Error

class Game:
    """ Handles scenes and the functionality of the entire game """
    def __init__(self):
        """ Loads game data and needed scene objects """

        self.constants = util.loadJson("data/constants.json")

        util.imgScale = self.constants["game"]["imgScale"]

        # Setup logging
        util.setupLogger(self.constants)

        # Class logger
        self.log = logging.getLogger(__name__)

        # Init objects
        self.log.info("Loading game scene")
        self.window = Window(self.constants)
        self.round = Round("amapwow", self.constants)
        
        # Error menu handler
        self.errorUI = Error(self.constants, self.round.getUIData())
    

    def startLoop(self):
        """ Game loop, with window updating and rendering, inputs, and game content """
        
        while not self.window.isClosed() and not self.errorUI.hasCrashed():
            self.window.handleInputs()
            
            self.errorUI.update(self.window)
            
            if not self.errorUI.isDisplaying():
                if self.errorUI.hasCrashed():
                    break # User pressed "Close Game"

            if not self.errorUI.isDisplaying():
                try:
                    self.round.update(self.window, self.constants)
                    self.round.render(self.window, self.constants)
                except Exception as exc:
                    Error.createError("An unhandled error occured while the game was running.", self.log, exc)
                
            else:
                self.errorUI.render(self.window)

            
            self.window.update(self.constants)