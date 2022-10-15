import pygame
import logging

import src.tile as tile
import src.utility as util

class Tileset:
    """ Manages the tiles and towers"""
    def __init__(self, map, consts):
        """ Initiates tileset """
        self.log = logging.getLogger(__name__)
        
        self.layout = self.loadTiles(map, consts)
        
        self.createTiles(self.layout, map, consts)
    

    @classmethod
    def loadTiles(cls, map, consts):
        """ Loads and creates all tiles needed for the tileset """
        file = util.loadFile(f"{consts['map']['paths']['maps']}/{map}/layout.txt")
        
        layout = []

        for row in file.split("\n"): # Iterate through all the rows 
            layout.append(list(row))
        
        return layout
    
    
    def createTiles(self, layout, map, consts):
        """ Creates each Tile object for every tile in the map """
        tileJson = util.loadJson(f"{consts['map']['paths']['maps']}/{map}/tiles.json")

        self.tiles = []
        
        for y, row in enumerate(layout):
            rowList = []

            for x, type in enumerate(row):
                rowList.append(tile.Tile(type, (x, y), consts, tileJson))
            
            self.tiles.append(rowList)
        
    
    def render(self, window):
        """ Renders all tiles in the tileset """
        for row in self.tiles:
            for tile in row:
                tile.render(window)