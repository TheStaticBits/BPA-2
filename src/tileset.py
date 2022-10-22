import pygame
import logging

import src.tile as tile
import src.utility as util
from src.vector import Vect

class Tileset:
    """ Manages the tiles and towers"""
    def __init__(self, map, consts):
        """ Initiates tileset """
        self.log = logging.getLogger(__name__)
        
        self.layout = self.loadTiles(map, consts)
        
        self.createTiles(self.layout, map, consts)
    

    def loadTiles(self, map, consts):
        """ Loads and returns tileset layout text file """
        self.log.info(f"Loading map \"{map}\"")

        file = util.loadFile(f"{consts['mapPaths']['maps']}/{map}/{consts['mapPaths']['layoutFile']}")
        
        layout = []

        for row in file.split("\n"): # Iterate through all the rows 
            layout.append(list(row))
        
        return layout
    
    
    def createTiles(self, layout, map, consts):
        """ Creates each Tile object for every tile in the map """
        self.log.info(f"Generating tiles for \"{map}\"")

        self.tileJson = util.loadJson(f"{consts['mapPaths']['maps']}/{map}/{consts['mapPaths']['tilesJson']}")

        self.tiles = []
        
        for y, row in enumerate(layout):
            rowList = []

            for x, type in enumerate(row):
                rowList.append(tile.Tile(type, (x, y), self.tileJson))
            
            self.tiles.append(rowList)
    

    def update(self, window, consts):
        """ New frame, updates all tiles """
        for row in self.tiles:
            for tile in row:
                tile.update(window, consts)
    

    def renderTiles(self, window):
        """ Renders only the square tile image, no deco """
        for row in self.tiles:
            for tile in row:
                tile.render(window)
    
    
    def renderDeco(self, window):
        """ Renders any decoration on the tiles"""
        for row in self.tiles:
            for tile in row:
                tile.renderDeco(window)

    # Getters
    def getTileAt(self, coords): 
        if coords.x < len(self.tiles[0]) and coords.y < len(self.tiles):
            return self.tiles[coords.y][coords.x]
        else: return False # Out of index

    def getTileJson(self): return self.tileJson

    def getBoardSize(self):
        tileSize = self.tiles[0][0].getSize()
        size = Vect(len(self.tiles[0]), len(self.tiles)) * tileSize
        return size