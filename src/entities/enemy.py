from inspect import _void
import pygame
import logging
import random

import src.utility.utility as util
import src.utility.animation as anim
import src.entities.entity as entity
from src.utility.timer import Timer
from src.utility.vector import Vect

class Enemy(entity.Entity):
    """ Any enemies are inherited from this class.
        Handles enemy movement and enemy animations. """

    # Moving: ------------ Left ------- Up -------- Right ----- Down
    DIR_CLOCKWISE = [ Vect(-1, 0), Vect(0, -1), Vect(1, 0), Vect(0, 1) ]

    def __init__(self, type, tileset, enemiesJson):
        self.log = logging.getLogger(__name__)

        self.reachedEnd = False
        
        self.speed =  enemiesJson[type]["speed"]
        self.health = enemiesJson[type]["health"]

        self.dropAmount = enemiesJson[type]["dropAmount"]
        self.dropChances = enemiesJson[type]["dropChances"]

        if "ability" in enemiesJson[type]:
            self.ability = enemiesJson[type]["ability"]["execute"]
            self.abilityTimer = Timer(enemiesJson[type]["ability"]["delay"])
        else:
            self.ability = None

        tileJson = tileset.getTileJson()

        # Gets start tile
        startTile = tileset.getTileAt(Vect(tileJson["start"]["tile"]))
        self.moveDir = Vect(tileJson["start"]["facingDir"])
        self.nextTile = startTile.getCoords() # Moving to start tile from offscreen

        animData = enemiesJson[type]["animation"]
        super().__init__(animData) # sets up animation 
        
        # Position offscreen, moving onto the start tile
        pos = self.getPosOnTile(startTile) - (self.moveDir * startTile.getSize())
        super().setPos(pos) # setup position


    def update(self, window, tileset):
        """ updates animation and position of enemy """
        
        super().updateAnim(window)

        # Move
        super().addToPos(self.moveDir * (self.speed * window.getDeltaTime()))
        
        # Reached the next tile destination
        onTile = tileset.getTileAt(self.nextTile)
        if self.onNextTile(window, onTile): # turn to next tile and set dest

            super().setPos(self.getPosOnTile(onTile)) # center on tile
            self.turn(onTile.getMoveDir())
            
            # moving destination by one board coordinate
            self.nextTile = onTile.getCoords() + self.moveDir
        
        self.updateAbility(window)
    

    def updateAbility(self, window):
        """ Updates ability timer if there is one """
        if self.ability != None:
            self.abilityTimer.update(window)

            if self.abilityTimer.activated():
                exec(self.ability) 
    

    def onNextTile(self, window, tile):
        """ Tests if the enemy has reached the next tile """
        
        if tile == False: # Moved off board
            self.reachedEnd = True
            return False
        
        # Finding difference in x/y between the tile and where it needs to move to
        diff = (self.getPosOnTile(tile) - super().getPos()).abs()

        # amount moved per frame
        frameDistance = self.speed * window.getDeltaTime()

        # Tile within one frame of movement from the destination
        return diff.x <= frameDistance and diff.y <= frameDistance
    
    
    def turn(self, direction):
        """ Implements turning left, right, and turning around """
        index = self.DIR_CLOCKWISE.index(self.moveDir)

        if direction == "forward": return None      # No turning
        elif direction == "right":       index += 1 # Clockwise
        elif direction == "left":        index -= 1 # Counterclockwise
        elif direction == "turn around": index += 2 # Turn around

        # Wrap around the list, end or start
        if index >= len(self.DIR_CLOCKWISE): 
            index -= len(self.DIR_CLOCKWISE)
        elif index < 0: 
            index = len(self.DIR_CLOCKWISE) - 1
        
        self.moveDir = self.DIR_CLOCKWISE[index]
    

    def takeDamage(self, amount):
        """ Enemy takes damage of amount """
        self.health -= amount

        # Future effects upon enemy death here
    
    
    def getPosOnTile(self, tile):
        return tile.getCenter() - (super().getAnim().getSize() / 2)
    

    def hasReachedMapEnd(self, tileset):
        """ Returns true if the enemy has moved off the screen """
        if not self.reachedEnd: return False

        # Check if on board
        return not util.rectCollision(super().getPos(), super().getAnim().getSize(),
                                      Vect(0, 0),       tileset.getBoardSize())
    
    def isDead(self, tileset):
        """ Returns true if the enemy has died """
        return self.health <= 0

    def getDamage(self):
        return self.health
        # Damage done to the player's health upon reaching the end,
        # the health remaining on the enemy is dealt to the player's health as 

    
    def getDrops(self):
        """ Returns a dictionary of how much of each resource the enemy dropped """
        drops = { "wood": 0, "steel": 0, "uranium": 0 }

        for i in range(self.dropAmount):
            num = random.randint(0, 100)

            # Matches up the random number with a drop chance and 
            # adds one drop to the resource randomly chosen
            for resource, chance in self.dropChances.items():
                if num <= chance:
                    drops[resource] += 1
                    break
                else:
                    num -= chance
        
        return drops