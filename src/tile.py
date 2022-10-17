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
            
            self.deco = anim.Animation(path, animData["frames"], animData["delay"])

            self.decoOffset = tileJson["deco"][type]["offset"]


        self.loadTex(type, consts, tileJson)

        # Gets tile type
        t = self.decoTile if self.isDeco else type

        # Coordinates given multiplied by the tile size
        self.pos = [ coord[0] * self.textures[t].get_width(),
                     coord[1] * self.textures[t].get_height() ]
    
    
    def loadTex(self, type, consts, tileJson):
        """ Loads texture into class variable if it hasn't already been loaded """
        # Decoration tile
        if self.isDeco: type = self.decoTile
        
        # don't continue if the tile img is already loaded
        if type in self.textures: return None
        
        # consts contains the path to the tiles image folder
        path = f"{consts['map']['paths']['tiles']}/{tileJson['tiles'][type]['img']}"
        
        self.textures[type] = util.loadTexTransparent(path)
    

    def update(self, window):
        """ Updates decoration animation if there is one """
        if self.isDeco: self.deco.update(window) 

    
    def render(self, window): # window is the Window object
        """ Render the tile itself """ 

        if self.isDeco: type = self.decoTile
        else:           type = self.type

        window.render(self.textures[type], self.pos)
    
    
    def renderDeco(self, window):
        """ Renders the decoration at the offset if there's any deco """
        if not self.isDeco: return None

        # Centers image on the offset from the tile
        pos = ( self.pos[0] + self.decoOffset[0] - (self.deco.getWidth()  // 2),
                self.pos[1] + self.decoOffset[1] - (self.deco.getHeight() // 2))
        
        self.deco.render(window, pos)