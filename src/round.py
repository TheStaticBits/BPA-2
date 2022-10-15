import pygame
import logging

import src.tileset as tileset

class Round:
    """ Handles the game content, such as the world, tileset, and towers """

    def __init__(self, map, consts):
        """ Setup tileset object, etc. """
        self.log = logging.getLogger(__name__)

        self.tileset = tileset.Tileset(map, consts)
    
    
    def render(self, window):
        """ Render tileset and eventually towers"""
        self.tileset.render(window)