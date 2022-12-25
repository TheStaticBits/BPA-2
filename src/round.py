import pygame
import logging

import src.utility.utility as util
from src.tileset import Tileset
from  src.entities.tower import Tower
from src.waves import Waves
from src.ui.shop import Shop
from src.ui.upgrade import UpgradeMenu
from src.ui.error import Error

class Round:
    """ Handles the game content, such as the world, tileset, and towers
        for every game that the player plays. """
    
    towersJson = None
    shopData = None

    def __init__(self, map, consts, uiData):
        """ Setup tileset object, etc. """
        self.log = logging.getLogger(__name__)

        self.tileset = Tileset(map, consts)
        self.waves = Waves(consts)
        
        try:
            self.towersJson = util.loadJson(consts["jsonPaths"]["towers"])
        except KeyError as exc:
            Error.createError("Unable to find the required paths to JSON files within the constants JSON.", self.log, exc)

        self.shop = Shop(consts, uiData, self.towersJson)
        self.upgradeMenu = UpgradeMenu(consts, uiData)
        
        self.towers = []

        self.resources = { "wood": 20, "steel": 0, "uranium": 0, "plasma": 0 }
    
    
    def update(self, window, consts):
        """ Updates everything for the frame """
        self.tileset.update(window, consts)
        self.waves.update(window, self.tileset)
        self.addDrops(self.waves.getFrameDrops())

        self.shop.update(window, self.resources, self.upgradeMenu.isDisplaying())
        self.upgradeMenu.update(window)

        self.checkPurchases()
        self.updateTowers(window, consts)
        
        if window.getMouseReleased("right"):
            if not self.isPlacingATower():
                self.unselectTowers()
                self.towers.append(Tower("Placeholder bro", self.towersJson))


    def updateTowers(self, window, consts):
        """ Updates towers and tower selecting"""
        noTowers = True

        for tower in self.towers:
            tower.update(window, self.tileset, self.waves, consts)

            if tower.justSelected(): 
                if not self.isPlacingATower(): # If not currently placing a tower
                    self.upgradeMenu.selectTower(tower) # Display upgrades
                    
                else:
                    # A tower is being placed, and the player just clicked on a different tower
                    tower.unselect()
            
            if tower.isSelected(): noTowers = False

        if self.upgradeMenu.isDisplaying() and noTowers:
            self.upgradeMenu.setDisplaying(False)
    

    def purchase(self, price):
        """ Decreases the player's currency by the amount given """
        for resName in self.resources.keys():
            self.resources[resName] -= price[resName]


    def checkPurchases(self):
        """ Checks and handles the event of the player pressing the "buy" button """
        if self.shop.getBought():
            # Charging the player for the resources
            self.purchase(self.shop.getTowerPrice())
            # Adding the tower to the tower list
            self.towers.append(Tower(self.shop.getSelectedTowerName(), self.towersJson))
        
        #

    
    def addDrops(self, drops):
        """ Adds resources dropped from the enemy to the player's money """
        for resource, amount in drops.items():
            self.resources[resource] += amount
    
    
    def render(self, window, consts):
        """ Render tileset, enemies, and towers """
        self.tileset.renderTiles(window)
        self.tileset.renderDeco(window)
        self.waves.render(window)
        self.shop.render(window)
        self.upgradeMenu.render(window)

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
    

    def unselectTowers(self):
        """ Unhighlights every tower, turning off showRange """
        for tower in self.towers:
            tower.unselect()