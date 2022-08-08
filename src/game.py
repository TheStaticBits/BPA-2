import pygame
import logging
import json

import src.utility
import src.window

log = logging.getLogger(__name__)

class Game:
    def __init__(self):
        """ Loads game data and needed scene classes """
        self.load_constants()
        pygame.init()

        self.window = src.window.Window(self.constants)
    
    
    def load_constants(self):
        """ Loads constants file for constant data values within the game """
        with open("data/constants.json") as f:
            self.constants = json.load(f)
    

    def start_loop(self):
        """ Game loop """
        
        while not self.window.close:
            self.window.handle_inputs()

            self.window.update(self.constants)