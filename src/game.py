import pygame
import logging

import src.utility
import src.window

class Game:
    def __init__(self):
        """ Loads game data and needed scene classes """

        self.constants = src.utility.load_constants()

        # Setup logging
        src.utility.setup_logger(self.constants)

        # Class logger
        self.log = logging.getLogger(__name__)

        self.window = src.window.Window(self.constants)
    

    def start_loop(self):
        """ Game loop """
        
        while not self.window.close:
            self.window.handle_inputs()

            self.window.update(self.constants)