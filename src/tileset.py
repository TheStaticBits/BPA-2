import pygame
import logging

import src.utility.utility as util
from src.entities.tile import Tile
from src.utility.vector import Vect
from src.ui.error import Error

class Tileset:
    """ Manages the tiles and towers"""
    def __init__(self, map, consts):
        """ Initiates tileset """
        self.log = logging.getLogger(__name__)
        
        self.layout = self.loadTiles(map, consts)
        self.offset = Vect(consts["game"]["mapOffset"])
        
        self.createTiles(self.layout, map, consts)
    

    def loadTiles(self, map, consts):
        """ Loads and returns tileset layout text file """
        self.log.info(f"Loading map \"{map}\"")

        try:
            file = util.loadFile(f"{consts['mapPaths']['maps']}/{map}/{consts['mapPaths']['layoutFile']}")

        except KeyError as exc:
            Error.createError("Unable to find required map path data within the constants file", self.log, exc)
        
        layout = []

        for row in file.split("\n"): # Iterate through all the rows 
            layout.append(list(row))
        
        return layout
    
    
    def createTiles(self, layout, map, consts):
        """ Creates each Tile object for every tile in the map """
        self.log.info(f"Generating tiles for \"{map}\"")

        try:
            mapDataJson = util.loadJson(f"{consts['mapPaths']['maps']}/{map}/{consts['mapPaths']['mapDataJson']}")

            self.tileJson = util.loadJson(mapDataJson["tileset"])
            self.enemyStartPos = mapDataJson["start"]
        
        except KeyError as exc:
            Error.createError("Unable to find required map tile JSON path data within the constants file", self.log, exc)

        self.tiles = []
        
        for y, row in enumerate(layout):
            rowList = []

            for x, type in enumerate(row):
                pos = Vect(x, y) + self.offset
                rowList.append(Tile(type, pos, self.tileJson))
            
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
    
    
    def renderToSurf(self, surface):
        """ Renders tiles to a Pygame Surface """
        for row in self.tiles:
            for tile in row:
                tile.render(surface, surf=True)
    
    
    def renderDeco(self, window):
        """ Renders any decoration on the tiles"""
        for row in self.tiles:
            for tile in row:
                tile.renderDeco(window)

    # Getters
    def getTileAt(self, coords): 
        """ Returns the tile at the given board coordinates,
            returns False if the coordinates are outside of the tileset """
        if coords.x < len(self.tiles[0]) and coords.y < len(self.tiles):
            return self.tiles[coords.y][coords.x]
        else: return False # Out of index
    
    def getMouseTile(self):
        """ Finds and returns the tile that the mouse is on,
            or returns False if the mouse is not on a tile """ 
        for row in self.tiles:
            for tile in row:
                if tile.mouseIsOnTile():
                    return tile
        
        return False
        

    def getTileJson(self): return self.tileJson
    def getEnemyStartPos(self): return self.enemyStartPos
    
    def getTilesSize(self): return Vect(len(self.tiles[0]), len(self.tiles))

    def getBoardSize(self):
        tileSize = self.tiles[0][0].getSize().x
        size = self.getTilesSize() * tileSize
        return size