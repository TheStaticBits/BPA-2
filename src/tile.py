import pygame
import logging

import src.utility as util
import src.animation as anim
from src.vector import Vect

class Tile:
    """ Handles each tile and the images and functionality """
    
    textures = {} # Dict, {tileTypeChar: pygame.Surface} 

    def __init__(self, type, coord, consts, tileJson):
        """ Setup tile """
        self.log = logging.getLogger(__name__)
        
        self.coord = Vect(coord)

        self.loadTileData(type, consts, tileJson)
        self.loadTex(consts, tileJson)

        # Coordinates given multiplied by the tile size
        # (position on screen)
        self.pos = Vect(coord) * Vect(self.textures[self.type].get_size())

    
    def loadTileData(self, type, consts, tileJson):
        self.isDeco = type in tileJson["deco"]
        self.rotate = None

        if self.isDeco:
            self.type = tileJson["deco"][type]["tile"] # Tile type of the tile behind deco
            self.decoTile = type
            self.decoOffset = Vect(tileJson["deco"][type]["offset"])

            animData = tileJson["deco"][type]["animation"]
            # Folder path + file in folder path
            path = f"{consts['map']['paths']['tiles']}/{animData['img']}" 

            self.deco = anim.Animation(path, animData["frames"], animData["delay"])

        else:
            if type in tileJson["rotated"]:
                self.rotate = tileJson["rotated"][type]["degrees"]
                type = tileJson["rotated"][type]["tile"]
            
            if type not in tileJson["tiles"]:
                self.log.error(f"Tile \"{type}\" not declared in tiles.json")
            
            self.type = type
            self.move = tileJson["tiles"][type]["move"]
            
                
    def loadTex(self, consts, tileJson):
        """ Loads texture into class variable if it hasn't already been loaded """
        
        # don't continue if the tile img is already loaded
        if self.type in self.textures: return None
        
        # load image
        path = f"{consts['map']['paths']['tiles']}/{tileJson['tiles'][self.type]['img']}"
        self.textures[self.type] = util.loadTexTransparent(path)


    def update(self, window):
        """ Updates decoration animation if there is one """
        if self.isDeco: self.deco.update(window)

    
    def render(self, window): # window is the Window object
        """ Render the tile itself """ 
        tex = self.textures[self.type]

        if self.rotate != None: 
            pygame.transform.rotate(tex, self.rotate)
        
        window.render(tex, self.pos)
    
    
    def renderDeco(self, window):
        """ Renders the decoration at the offset if there's any deco """
        if not self.isDeco: return None

        # Centers image on the offset from the tile
        pos = (self.pos + self.decoOffset - (self.deco.getSize() // 2))
        self.deco.render(window, pos)
    

    # Getters
    def getMoveDir(self):
        """ Gets enemy move direction for the tile """
        return False if self.isDeco else self.move

    def getCenter(self):
        """ Returns center of tile position """ 
        return self.pos + (self.getSize() // 2)
    
    def getSize(self):   return Vect(self.textures[self.type].get_size())
    def getWidth(self):  return self.getSize().x
    def getHeight(self): return self.getSize().y

    def getCoord(self): return self.coord
    def getPos(self): return self.pos