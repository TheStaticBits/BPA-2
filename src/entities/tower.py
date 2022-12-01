import pygame
import logging

import src.entities.entity as entity
from src.utility.timer import Timer
from src.utility.vector import Vect
from src.ui.error import Error

class Tower(entity.Entity):
    """ All towers inherit from this class.
        Manages the placement and rendering """
    
    # Tile parameter is the tile object the tower was placed on
    def __init__(self, type, towersJson): 
        self.log = logging.getLogger(__name__)

        animData = towersJson[type]["animation"]
        super().__init__(animData)
        
        try:
            self.upgradeInfo = towersJson[type]["upgrades"]
            self.damageFrame = towersJson[type]["dealDMGFrame"]
            self.attackMode = towersJson[type]["attackMode"]
        except KeyError as exc:
            Error.createError(f"Unable to find required data within the JSON file for the {type} tower.", self.log, exc)
            return None

        self.upgradeNum = 0
        
        self.type = type
        self.loadUpgrade(0) # Initial statistics

        # A bunch of default booleans used to tower actions
        self.placing = True
        self.showRange = True
        self.canBePlaced = False
        self.attacking = False
        self.waitingForEnemy = False
        self.clickedOn = False

        self.tileOn = None # Reference to the Tile object the tower is on
    

    def loadUpgrade(self, upgradeNum):
        """ Sets up variables from the tower statistics """
        try:
            self.range =  self.upgradeInfo[upgradeNum]["stats"]["range"]
            self.damage = self.upgradeInfo[upgradeNum]["stats"]["damage"]
            self.attackTimer = Timer( self.upgradeInfo[upgradeNum]["stats"]["attackCooldown"] )

        except KeyError as exc:
            Error.createError(f"Unable to find required update information for the upgrade number {upgradeNum} for the tower {type}.", self.log, exc)
    

    def getTowerPosOnTile(self, tile, consts):
        """ Finds the position of the tower on the tile """
        pos = tile.getCenter().copy()

        pos.x -= (super().getAnim().getWidth() // 2)

        try:
            pos.y += consts["towers"]["tileYOffset"] - super().getAnim().getHeight()

        except KeyError as exc:
            Error.createError("Unable to find tileYOffset for towers within the constants JSON file.", self.log, exc)

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
        """ Deals damage to the first enemy or all the enemies in the range
            depending on the attack mode """ 
        collided = self.getCollidedEnemies(waves)
        
        if self.attackMode == "one":
            if len(collided) != 0:
                collided[0].takeDamage(self.damage)
                # self.log.info("dealt damage")
        
        elif self.attackMode == "all":
            for tower in collided:
                tower.takeDamage(self.damage)
    

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
        self.clickedOn = False

        if not self.placing:
            self.updateAttack(window, wavesObj)

            if window.getMouseReleased("left"):
                if tileset.getMouseTile() == self.tileOn:
                    self.showRange = not self.showRange
                    
                    if self.showRange:
                        self.clickedOn = True
        
        else:
            posTile = tileset.getMouseTile() # Returns the tile the mouse is on
            
            if posTile != False: # Mouse is on a tile
                # new tile position
                if posTile != self.tileOn:
                    super().setPos(self.getTowerPosOnTile(posTile, consts))
                    self.tileOn = posTile
                
                self.canBePlaced = posTile.canBePlacedOn() and not posTile.getHasTower()
            
            else:
                self.tileOn = None
                self.canBePlaced = False
            
            if self.canBePlaced and window.getMouseReleased("left"): # Placed
                self.placing = False
                self.showRange = False
                self.tileOn.placedTower()
    

    def render(self, window, consts):
        """ Renders the tower to the screen, 
            with range circle if selected,
            and with transparency if being placed. """

        # Does not render if the mouse is not on any tile
        if self.tileOn == None: return None 

        if self.showRange:
            # Render range circle
            try:
                if self.canBePlaced: color = consts["towers"]["rangeCircleGreen"]
                else:                color = consts["towers"]["rangeCircleRed"]
            
            except KeyError as exc:
                Error.createError("Unable to find tower range circle color data within the constants JSON file.", self.log, exc)
            
            # Center circle on the tower
            window.render(self.getRangeCircle(color), self.getCirclePos())
        
        if self.tileOn == None: offset = 0
        else: offset = -self.tileOn.getHoverOffset()
        
        # Render tower at offset of the tile hovering effect
        super().render(window, yOffset=offset)
    

    def getCirclePos(self): 
        """ Finds the top left of where the range circle should be rendered"""
        return self.tileOn.getCenter() - self.range

    # Basic getters
    def getTileOn(self): return self.tileOn
    def isPlacing(self): return self.placing
    def isSelected(self): return self.showRange
    def justSelected(self): return self.clickedOn

    # Setters
    def unselect(self): self.showRange = False