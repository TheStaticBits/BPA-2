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
        self.waitingForEnemy = False

    
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
    

    def getTilesInRange(self, tileset):
        """ Returns a list of tiles that are within the range of the tower """
        range = Vect(self.range)

        # Creates a surface of width and height 
        rangeCollision = pygame.Surface((self.range * 2).getTuple())
        pos = super().getPos() - range

        return tileset.getCollidedTiles(rangeCollision, pos)

    
    def towerPosOnTile(self, tile, consts):
        """ Finds the position of the tower on the tile """
        pos = tile.getPos().copy()
        
        pos.x += (tile.getWidth() // 2) - (super().getAnim().getWidth() // 2)
        pos.y += tile.getHeight() - super().getAnim().getHeight() - consts["towers"]["tileYOffset"] - tile.getHoverOffset()

        return pos
    

    def getCollidedEnemies(self, waves):
        return waves.getCollided(super().getAnim().getImgFrame(), super().getPos())

    
    def dealDamage(self, waves):
        """ Deals damage to the first enemy in the range """ 
        collided = self.getCollidedEnemies(waves)
        
        if len(collided) != 0:
            collided[0].takeDamage(self.damage)
    
    
    def update(self, window, tileset, wavesObj, consts, towersJson):
        """ Updates animation if placed and when firing at an enemy """

        if not self.placing:
            # Switches between delay between attacks and attacking with animation updating
            if not self.attacking:
                self.attackTimer.update(window)
                if self.attackTimer.activated():
                    self.attacking = True
                    self.waitingForEnemy = True
            
            else:
                if not self.waitingForEnemy:
                    super().updateAnim(window)

                    if super().getAnim().getFrameNum() == towersJson[self.type]["dealDMGFrame"]:
                        self.dealDamage(wavesObj)

                    if super().getAnim().finished():
                        self.attacking = False

                elif len(self.getCollidedEnemies(wavesObj)) != 0:
                    self.waitingForEnemy = False
        
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
            if self.canBePlaced: color = consts["towers"]["rangeCircleGreen"]
            else:                color = consts["towers"]["rangeCircleRed"]
            
            range = Vect(self.range)

            # Create transparent circle with radious as self.range
            circleSurf = pygame.Surface((range * 2).getTuple(), pygame.SRCALPHA)
            pygame.draw.circle(circleSurf, color, range.getTuple(), self.range)

            # Center circle on the tower
            window.render(circleSurf, super().getPos() + (super().getAnim().getSize() // 2) - self.range)

        
        if self.placing and not self.canBePlaced:
            # Render with a red tint
            
            img = super().getAnim().getImgFrame()
            size = super().getAnim().getSize()

            # Semi-transparent red image
            redSurf = pygame.Surface(size.getTuple(), flags=pygame.SRCALPHA)
            redSurf.fill(consts["towers"]["redOverlayColor"])
            
            # Blend red onto the tower image
            img.blit(redSurf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            window.render(img, super().getPos())
        
        else:
            # Render normally
            super().render(window)