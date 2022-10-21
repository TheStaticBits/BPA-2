import pygame
import logging

import src.utility as util
import src.tileset as tileset
import src.waves as waves

class Round:
    """ Handles the game content, such as the world, tileset, and towers
        for every game that the player plays. """

    def __init__(self, map, consts):
        """ Setup tileset object, etc. """
        self.log = logging.getLogger(__name__)

        self.tileset = tileset.Tileset(map, consts)
        self.waves = waves.Waves(consts)
    
    
    def update(self, window):
        """ Updates everything for the frame """
        self.tileset.update(window)
        self.waves.update(window, self.tileset)
    
    
    def render(self, window):
        """ Render tileset, enemies, and towers """
        self.tileset.renderTiles(window)
        self.tileset.renderDeco(window)
        self.waves.render(window)