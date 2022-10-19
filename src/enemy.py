import pygame
import logging

import src.utility as util
import src.animation as anim
from src.vector import Vect

class Enemy:
    """ Any enemies are inherited from this class.
        Handles enemy movement and enemy animations. """

    DIR_TO_VERTEX = { "left":  Vect(-1,  0),
                      "right": Vect( 1,  0),
                      "up":    Vect( 0, -1),
                      "down":  Vect( 0,  1) }

    def __init__(self, type, startTile, enemiesJson, consts):
        self.log = logging.getLogger(__name__)

        self.anim = anim.Animation(enemiesJson[type]["animation"])

        givenDir = startTile.getMoveDir().split(" ")
        if givenDir[0] != "startFrom": self.log.error("Enemy class given non-start tile")

        startFrom = self.DIR_TO_VERTEX[givenDir[1]]
        
        # Start from direction is the direction off screen from the tile,
        # so the direction the enemy has to move to get onto the tile
        # is the opposite of that direction.
        self.moveDir = startFrom * -1

        center = startTile.getCenter()
        self.pos = center + (startFrom * startTile.getSize()) - (self.anim.getSize() / 2)
                
        self.speed = enemiesJson[type]["speed"]
        self.health = enemiesJson[type]["health"]
    

    def update(self, window):
        """ updates animation and position of enemy """
        self.anim.update(window)

        # move position 
        self.pos += self.moveDir * self.speed * window.getDeltaTime()

        # update direction if enemy has moved onto a new tile
