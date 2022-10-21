import pygame
import logging

import src.utility as util
import src.animation as anim
from src.vector import Vect

class Enemy:
    """ Any enemies are inherited from this class.
        Handles enemy movement and enemy animations. """

    # Moving: ------------ Left ------- Up -------- Right ----- Down
    DIR_CLOCKWISE = [ Vect(-1, 0), Vect(0, -1), Vect(1, 0), Vect(0, 1) ]

    def __init__(self, type, tileset, enemiesJson):
        self.log = logging.getLogger(__name__)

        self.speed = enemiesJson[type]["speed"]
        self.health = enemiesJson[type]["health"]
        animData = enemiesJson[type]["animation"]
        self.anim = anim.Animation(animData["path"], animData["frames"], animData["delay"])

        tileJson = tileset.getTileJson()

        # Gets start tile
        startTile = tileset.getTileAt(Vect(tileJson["start"]["tile"]))
        self.moveDir = Vect(tileJson["start"]["facingDir"])
        self.nextTile = startTile.getCoord() # Moving to start tile from offscreen

        # Position offscreen, moving onto the start tile
        self.pos = self.getPosOnTile(startTile) - (self.moveDir * startTile.getSize())
    

    def turn(self, direction):
        """ Implements turning left, right, and turning around """
        index = self.DIR_CLOCKWISE.index(self.moveDir)

        # Clockwise, counter clockwise, turning around
        if direction == "right":         index += 1
        elif direction == "left":        index -= 1
        elif direction == "turn around": index += 2

        # Wrap around the list, end or start
        if index >= len(self.DIR_CLOCKWISE): 
            index -= len(self.DIR_CLOCKWISE)
        elif index < 0: 
            index = len(self.DIR_CLOCKWISE) - 1
        
        self.moveDir = self.DIR_CLOCKWISE[index]

    
    def getPosOnTile(self, tile):
        return tile.getCenter() - (self.anim.getSize() / 2)

    
    def findNextTile(self, currentTile):
        """ Finds next tile to move to based on given direction """

        tileMoveDir = currentTile.getMoveDir()

        if tileMoveDir == False:
            self.log.error("Enemy moved onto a non-move tile")

        self.turn(currentTile.getMoveDir())
        self.nextTile = currentTile.getCoord() + self.moveDir
    

    def onNextTile(self, window, tileset):
        """ Tests if the enemy has reached the next tile """
        moveToTile = tileset.getTileAt(self.nextTile)
        
        # Finding difference in x/y between the tile and where it needs to move to        
        diff = (moveToTile.getPos() - self.pos).abs()

        # amount moved per frame
        frameDistance = self.speed * window.getDeltaTime()

        # Tile within one frame of movement from the destination
        return diff.x <= frameDistance or diff.y <= frameDistance


    def update(self, window, tileset):
        """ updates animation and position of enemy """
        
        self.anim.update(window)

        # Move
        self.pos += self.moveDir * self.speed * window.getDeltaTime()
        
        if (self.onNextTile(window, tileset)):
            self.findNextTile(self.nextTile) 
            # nextTile would be the tile the enemy is currently on


    def render(self, window):
        """ Render enemy """

        self.anim.render(window, self.pos.getTuple())

        # Difference between the position the enemy is at 
        # and the next tile