import pygame
import logging

import src.utility as util
import src.animation as anim

class Tile:
    """ Handles each tile and the images and functionality """
    
    textures = {} # Dict, {tileTypeChar: pygame.Surface} 

    def __init__(self, type, coord, consts, tileJson):
        """ Setup tile """
        self.log = logging.getLogger(__name__)
        
        self.type = type


        self.isDeco = type in tileJson["deco"] # Deco = Decoration
        if not self.isDeco:
            # Direction the tile moves enemies (deco tiles cannot move enemies)
            self.move = tileJson["tiles"][type]["move"]
        else:
            # Tile type of the tile behind deco
            self.decoTile = tileJson["deco"][type]["tile"]

            # Animation of decoration on the tile
            animData = tileJson["deco"][type]["animation"]

            # Folder path + the given path to the file
            path = f"{consts['map']['paths']['tiles']}/{animData['img']}"
            
            self.deco = anim.Animation(path, animData)

            self.decoOffset = Vect(tileJson["deco"][type]["offset"])

        self.loadTex(type, consts, tileJson)

        # Gets tile type
        t = self.getTileType()

        # Coordinates given multiplied by the tile size
        self.pos = Vect(coord) * Vect(self.textures[t].get_size())
    
    
    def loadTex(self, type, consts, tileJson):
        """ Loads texture into class variable if it hasn't already been loaded """
        # Decoration tile
        if self.isDeco: type = self.decoTile
        
        # don't continue if the tile img is already loaded
        if type in self.textures: return None
        
        # consts contains the path to the tiles image folder
        path = f"{consts['map']['paths']['tiles']}/{tileJson['tiles'][type]['img']}"

        img = util.loadTexTransparent(path)

        # rotate option
        if "rotate" in tileJson["tiles"][type]:
            self.textures[type] = pygame.transform.rotate(img, tileJson["tiles"][type]["rotate"])
        else:
            self.textures[type] = img


    def update(self, window):
        """ Updates decoration animation if there is one """
        if self.isDeco: self.deco.update(window)

    
    def render(self, window): # window is the Window object
        """ Render the tile itself """ 
        window.render(self.textures[self.getTileType()], self.pos)
    
    
    def renderDeco(self, window):
        """ Renders the decoration at the offset if there's any deco """
        if not self.isDeco: return None

        # Centers image on the offset from the tile
        pos = (self.pos + self.decoOffset - (self.deco.getSize() // 2))
        
        self.deco.render(window, pos)
    

    # Getters
    def getMoveDir(self):
        """ Gets enemy move direction for the tile """
        if self.isDeco: return False
        return self.move

    def getCenter(self):
        """ Returns center of tile position """ 
        return self.pos + (self.getSize() // 2)
    
    def getSize(self):   return Vect(self.textures[self.getTileType()].get_size())
    def getWidth(self):  return self.getSize().x
    def getHeight(self): return self.getSize().y

    def getTileType(self): return (self.decoTile if self.isDeco else type)