import pygame
import logging

import src.utility as util
import src.tileset as tileset
import src.tower as tower
import src.waves as waves

class Round:
    """ Handles the game content, such as the world, tileset, and towers
        for every game that the player plays. """

    def __init__(self, map, consts):
        """ Setup tileset object, etc. """
        self.log = logging.getLogger(__name__)

        self.tileset = tileset.Tileset(map, consts)
        self.waves = waves.Waves(consts)
        self.towers = []

        towersJson = util.loadJson(consts["jsonPaths"]["towers"])
        
        # Temporary
        self.towers.append(tower.Tower("Placeholder bro", towersJson))
    
    
    def update(self, window, consts):
        """ Updates everything for the frame """
        self.tileset.update(window, consts)
        self.waves.update(window, self.tileset)

        for tower in self.towers:
            tower.update(window, self.tileset, self.waves, consts)
    
    
    def render(self, window, consts):
        """ Render tileset, enemies, and towers """
        self.tileset.renderTiles(window)
        self.tileset.renderDeco(window)
        self.waves.render(window)

        for tower in self.towers:
            tower.render(window, consts)