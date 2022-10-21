import pygame
import logging

from src.vector import Vect

class Tower:
    """ All towers inherit from this class.
        Manages the placement and rendering """
    
    # Tile parameter is the tile object the tower was placed on
    def __init__(self, tile): 
        pass
    
    
    def canPlace(self, position, tileset):
        pass
    
    
    def render(self, window):
        pass