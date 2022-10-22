from inspect import _void
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

        self.reachedEnd = False
        
        self.speed =  enemiesJson[type]["speed"]
        self.health = enemiesJson[type]["health"]
        self.damage = enemiesJson[type]["damage"]
        
        animData = enemiesJson[type]["animation"]
        self.anim = anim.Animation(animData["path"], animData["frames"], animData["delay"])

        tileJson = tileset.getTileJson()

        # Gets start tile
        startTile = tileset.getTileAt(Vect(tileJson["start"]["tile"]))
        self.moveDir = Vect(tileJson["start"]["facingDir"])
        self.nextTile = startTile.getCoord() # Moving to start tile from offscreen

        # Position offscreen, moving onto the start tile
        self.pos = self.getPosOnTile(startTile) - (self.moveDir * startTile.getSize())


    def update(self, window, tileset):
        """ updates animation and position of enemy """
        
        self.anim.update(window)

        # Move
        self.pos += self.moveDir * (self.speed * window.getDeltaTime())
        
        # Reached the next tile destination
        onTile = tileset.getTileAt(self.nextTile)
        if self.onNextTile(window, onTile): # turn to next tile and set dest

            self.pos = self.getPosOnTile(onTile) # center on tile
            self.turn(onTile.getMoveDir())
            
            # moving destination by one board coordinate
            self.nextTile = onTile.getCoord() + self.moveDir


    def render(self, window):
        """ Render enemy """
        self.anim.render(window, self.pos)
    

    def onNextTile(self, window, tile):
        """ Tests if the enemy has reached the next tile """
        
        if tile == False: # Moved off board
            self.reachedEnd = True
            return False
        
        # Finding difference in x/y between the tile and where it needs to move to
        diff = (self.getPosOnTile(tile) - self.pos).abs()

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
    
    
    def getPosOnTile(self, tile):
        return tile.getCenter() - (self.anim.getSize() / 2)
    

    def hasReachedMapEnd(self, tileset):
        if not self.reachedEnd: return False

        # Check if on board
        return not util.rectCollision(self.pos,   self.anim.getSize(),
                                      Vect(0, 0), tileset.getBoardSize())

    def getDamage(self):
        return self.damage 
        # Damage done to the player's health upon reaching the end