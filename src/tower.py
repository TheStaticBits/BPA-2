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
        self.damageFrame = towersJson[type]["dealDMGFrame"]
        self.upgradeNum = 0

        self.loadUpgrade(0) # Initial statistics

        self.placing = True
        self.showRange = True
        self.canBePlaced = False
        self.attacking = False
        self.waitingForEnemy = False

        self.tileOn = None # Reference to the Tile object the tower is on

    
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
    

    def getTowerPosOnTile(self, tile, consts):
        """ Finds the position of the tower on the tile """
        pos = tile.getCenter().copy()

        pos.x -= (super().getAnim().getWidth() // 2)
        pos.y += consts["towers"]["tileYOffset"] - super().getAnim().getHeight()

        return pos


    def towerPosOnTile(self, tile, consts):
        """ Gets the tower's render position, adds tile offset """
        pos = self.getTowerPosOnTile(tile, consts)
        pos.y -= tile.getHoverOffset()

        return pos


    def getRangeCircle(self, color=(255, 255, 255, 255)):
        """ Returns a circle texture of the range of the tower """
        range = Vect(self.range)

        # Create transparent circle with radius as self.range
        circleSurf = pygame.Surface((range * 2).getTuple(), pygame.SRCALPHA)
        pygame.draw.circle(circleSurf, color, range.getTuple(), self.range)

        return circleSurf
    

    def getCollidedEnemies(self, waves):
        return waves.getCollided(self.getRangeCircle(), self.getCirclePos())

    
    def dealDamage(self, waves):
        """ Deals damage to the first enemy in the range, overriden """ 
        collided = self.getCollidedEnemies(waves)
        
        if len(collided) != 0:
            collided[0].takeDamage(self.damage)
            self.log.info("dealt damage")
    

    def updateAttack(self, window, wavesObj):
        """ Updates delay between attacks, then updates attack 
            animation when a tower is in range and deals damage """
        if not self.attacking:
            self.attackTimer.update(window)
            if self.attackTimer.activated():
                self.attacking = True
                self.waitingForEnemy = True
        
        else:
            if self.waitingForEnemy:
                # Test to see if there is an enemy in the tower range
                if len(self.getCollidedEnemies(wavesObj)) != 0:
                    self.waitingForEnemy = False
                    # Allows the enemy to attack the frame it detects an enemy

            if not self.waitingForEnemy: # Attacking
                super().updateAnim(window)

                
                if super().getAnim().changedFrame():
                    # Animation reached frame on which it deals damage to enemies
                    if super().getAnim().getFrameNum() == self.damageFrame - 1:
                        self.dealDamage(wavesObj)

                # Finished attack animation
                if super().getAnim().finished():
                    self.attacking = False
    
    
    def update(self, window, tileset, wavesObj, consts):
        """ Updates animation if placed and when firing at an enemy """

        if not self.placing:
            self.updateAttack(window, wavesObj)

            if window.getMouseReleased("left"):
                if tileset.getMouseTile() == self.tileOn:
                    self.showRange = not self.showRange
        
        else:
            posTile = tileset.getMouseTile() # Returns the tile the mouse is on
            
            if posTile != False: # Mouse is on a tile
                # new tile position
                if posTile != self.tileOn:
                    super().setPos(self.getTowerPosOnTile(posTile, consts))
                    self.tileOn = posTile
                
                self.canBePlaced = posTile.canBePlacedOn()
            
            else:
                self.tileOn = None
                self.canBePlaced = False
            
            if self.canBePlaced and window.getMouseReleased("left"): # Placed
                self.placing = False
                self.showRange = False
    

    def render(self, window, consts):
        """ Renders the tower to the screen, 
            with range circle if selected,
            and with transparency if being placed. """

        # Does not render if the mouse is not on any tile
        if self.tileOn == None: return None 

        if self.showRange:
            # Render range circle
            if self.canBePlaced: color = consts["towers"]["rangeCircleGreen"]
            else:                color = consts["towers"]["rangeCircleRed"]
            
            # Center circle on the tower
            window.render(self.getRangeCircle(color), self.getCirclePos())
        
        if self.tileOn == None: offset = 0
        else: offset = -self.tileOn.getHoverOffset()
        
        # Render tower at offset of the tile hovering effect
        super().render(window, yOffset=offset)
    

    def getCirclePos(self): 
        """ Finds the top left of where the range circle should be rendered"""
        return self.tileOn.getCenter() - self.range