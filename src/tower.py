import pygame
import logging

import src.entity as entity
from src.vector import Vect

class Tower(entity.Entity):
    """ All towers inherit from this class.
        Manages the placement and rendering """
    
    # Tile parameter is the tile object the tower was placed on
    def __init__(self, tile): 
        self.log = logging.getLogger(__name__)
        pass
    
    
    def canPlace(self, position, tileset):
        pass
    
    
    def render(self, window):
        pass