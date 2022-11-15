import pygame
import logging

import src.utility.utility as util
import src.tileset as tileset
import src.entities.tower as tower
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

        self.towersJson = util.loadJson(consts["jsonPaths"]["towers"])
        
        # Temporary
        self.towers.append(tower.Tower("Placeholder bro", self.towersJson))
    
    
    def update(self, window, consts):
        """ Updates everything for the frame """
        self.tileset.update(window, consts)
        self.waves.update(window, self.tileset)

        for t in self.towers:
            t.update(window, self.tileset, self.waves, consts)

        if window.getMouseReleased("right"):
            self.towers.append(tower.Tower("Placeholder bro", self.towersJson))
    
    
    def render(self, window, consts):
        """ Render tileset, enemies, and towers """
        self.tileset.renderTiles(window)
        self.tileset.renderDeco(window)
        self.waves.render(window)

        self.renderTowers(window, consts)
    
    
    def renderTowers(self, window, consts):
        """ Renders towers in order from the top to the bottom of the map
            in order to prevent tower overlap in the wrong direction """

        height = self.tileset.getTilesSize().y

        for row in range(height):
            for tower in self.towers:
                if tower.getTileOn() == None: continue

                elif tower.getTileOn().getCoords().y == row:
                    tower.render(window, consts)