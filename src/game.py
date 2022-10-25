import pygame
import logging

import src.utility as util
import src.window as window
import src.round as round

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
        self.window = window.Window(self.constants)
        self.round = round.Round("amapwow", self.constants)
    

    def start_loop(self):
        """ Game loop """
        
        while not self.window.isClosed():
            self.window.handleInputs()

            self.round.update(self.window, self.constants)
            self.round.render(self.window, self.constants)
            
            self.window.update(self.constants)