import pygame
import logging

import src.utility as util
import src.animation as anim
from src.vector import Vect

class Enemy:
    """ Any enemies are inherited from this class.
        Handles enemy movement and enemy animations. """

    DIR_TO_VECT = { "left":  Vect(-1,  0),
                    "right": Vect( 1,  0),
                    "up":    Vect( 0, -1),
                    "down":  Vect( 0,  1) }

    TURN_RIGHT = { (-1, 0) > (0, -1) > (1, 0) > (0, 1) > (-1, 0)}

    def __init__(self, type, startTile, enemiesJson, consts):
        self.log = logging.getLogger(__name__)

        animData = enemiesJson[type]["animation"]
        self.anim = anim.Animation(animData["path"], animData["frames"], animData["delay"])

        givenDir = startTile.getMoveDir()

        startFrom = self.DIR_TO_VECT[givenDir[1]]

        # Start from direction is the direction off screen from the tile,
        # so the direction the enemy has to move to get onto the tile
        # is the opposite of that direction, onto the start tile
        self.moveDir = startFrom * -1
        self.nextTile = startTile.getCoord()

        self.pos = self.getPosOnTile(startTile) + (startFrom * startTile.getSize())
                
        self.speed = enemiesJson[type]["speed"]
        self.health = enemiesJson[type]["health"]

    
    def getPosOnTile(self, tile):
        return tile.getCenter() - (self.anim.getSize() / 2)

    
    def findNextTile(self, currentTile):
        """ Finds next tile to move to based on given direction """

        self.moveDir = self.DIR_TO_VECT[currentTile.getMoveDir()]
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