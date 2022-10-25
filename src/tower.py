import pygame
import logging

import src.entity as entity
from src.timer import Timer
from src.vector import Vect

class Tower(entity.Entity):
    """ All towers inherit from this class.
        Manages the placement and rendering """
    
    # Tile parameter is the tile object the tower was placed on
    def __init__(self, type, towersJson): 
        self.log = logging.getLogger(__name__)

        animData = towersJson[type]["animation"]
        super().__init__(animData)
        
        self.upgradeInfo = towersJson[type]["upgrades"]

        self.loadUpgrade(0) # Initial statistics

        self.placing = True
        self.showRange = True
        self.canBePlaced = False
        self.attacking = False

    
    @staticmethod
    def getCost(type, towersJson, upgradeNum):
        """ Finds the cost of the given tower type in the towers JSON file """
        return towersJson[type]["upgrades"][upgradeNum]["costs"]

    @staticmethod
    def getInitialCost(type, towersJson):
        """ Finds the initial cost of the given tower type in the towersJson file"""
        return Tower.getCost(type, towersJson, 0) # Initial cost is the "first" upgrade
    

    def loadUpgrade(self, upgradeNum):
        """ Sets up variables from the tower statistics """
        self.range =  self.upgradeInfo[upgradeNum]["stats"]["range"]
        self.damage = self.upgradeInfo[upgradeNum]["stats"]["damage"]
        self.attackTimer = Timer( self.upgradeInfo[upgradeNum]["stats"]["attackCooldown"] )
    

    def towerPosOnTile(self, tile, consts):
        """ Finds the position of the tower on the tile """
        pos = tile.getPos().copy()
        
        pos.x += (tile.getWidth() // 2) - (super().getAnim().getWidth() // 2)
        pos.y += tile.getHeight() - super().getAnim().getHeight() - consts["towers"]["tileYOffset"] - tile.getHoverOffset()

        return pos
    
    
    def update(self, window, tileset, consts):
        """ Updates animation if placed and when firing at an enemy """

        if not self.placing:
            # Switches between delay between attacks and attacking with animation updating
            if not self.attacking:
                self.attackTimer.update(window)
                if self.attackTimer.activated():
                    self.attacking = True
            
            else:
                super().updateAnim(window)

                if super().getAnim().finished():
                    self.attacking = False
        
        else:
            posTile = tileset.getMouseTile() # Returns the tile the mouse is on
            
            if posTile != False: # Mouse is on a tile
                super().setPos(self.towerPosOnTile(posTile, consts))
                self.canBePlaced = posTile.canBePlacedOn()
            
            if self.canBePlaced and window.getMouse("left"): # Placed
                self.placing = False
                self.showRange = False
    

    def render(self, window, consts):
        """ Renders the tower to the screen, 
            with range circle if selected,
            and with transparency if being placed. """ 

        if self.showRange:
            # Render range circle
            if self.canBePlaced: color = consts["towers"]["rangeCircleRed"]
            else:                color = consts["towers"]["rangeCircleGreen"]
            
            range = Vect(self.range)

            # Create transparent circle with radious as self.range
            circleSurf = pygame.Surface((range * 2).getTuple(), pygame.SRCALPHA)
            pygame.draw.circle(circleSurf, color, range.getTuple(), self.range)

            window.render(circleSurf, super().getPos() + (super().getAnim().getSize() // 2) - self.range)

        
        if self.placing and self.canBePlaced:
            # Render with a red tint
            
            img = super().getAnim().getImgFrame()
            size = super().getAnim().getSize()

            # Red image
            redSurf = pygame.Surface(size.getTuple(), flags=pygame.SRCALPHA)
            redSurf.fill(consts["towers"]["redOverlayColor"])
            
            # Blend red onto the tower image
            img.blit(redSurf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            window.render(img, super().getPos() + (super().getAnim().getSize() // 2) - self.range)
        
        else:
            # Render normally
            super().render(window)