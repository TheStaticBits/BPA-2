import pygame
import logging

import src.utility.utility as util
import src.tileset as tileset
from  src.entities.tower import Tower
import src.waves as waves
import src.ui.shop as shop

class Round:
    """ Handles the game content, such as the world, tileset, and towers
        for every game that the player plays. """
    
    towersJson = None
    shopData = None

    def __init__(self, map, consts):
        """ Setup tileset object, etc. """
        self.log = logging.getLogger(__name__)

        self.tileset = tileset.Tileset(map, consts)
        self.waves = waves.Waves(consts)
        
        self.uiData = util.loadJson(consts["jsonPaths"]["ui"])
        self.shop = shop.Shop(consts, self.uiData)
        
        self.towers = []

        self.towersJson = util.loadJson(consts["jsonPaths"]["towers"])
        
        # Temporary
        self.towers.append(Tower("Placeholder bro", self.towersJson))
    
    
    def update(self, window, consts):
        """ Updates everything for the frame """
        self.tileset.update(window, consts)
        self.waves.update(window, self.tileset)
        self.shop.update(window)

        for tower in self.towers:
            tower.update(window, self.tileset, self.waves, consts)

            if tower.justSelected(): 
                # Unselecting every tower besides the one just selected
                if not self.isPlacingATower():
                    self.unselectTowers(notTower=tower)
                else:
                    # A tower is being placed, and the player just clicked on a different tower
                    tower.unselect()

        if window.getMouseReleased("right"):
            if not self.isPlacingATower():
                self.unselectTowers()
                self.towers.append(Tower("Placeholder bro", self.towersJson))
    
    
    def render(self, window, consts):
        """ Render tileset, enemies, and towers """
        self.tileset.renderTiles(window)
        self.tileset.renderDeco(window)
        self.waves.render(window)
        self.shop.render(window)

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
    
    
    def isPlacingATower(self):
        """ Returns true if there is a tower being placed currently """

        for tower in self.towers:
            if tower.isPlacing():
                return True
        
        return False
    

    def unselectTowers(self, notTower=None):
        """ Unhighlights every tower except for notTower """
        for tower in self.towers:
            if tower != notTower:
                tower.unselect()