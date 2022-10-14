import pygame
import logger

import src.utility as util

class Tile:
    """ Handles each tile and the images and functionality """
    
    textures = {} # Dict, {tileTypeChar: pygame.Surface} 

    def __init__(self, type, coord, consts, tileJson):
        """ Setup tile """
        self.loadTex(type, consts, tileJson)

        self.type = type
        self.pos = [ coord[0] * textures[type].get_width(),
                     coord[1] * textures[type].get_height() ]
        
        if type in tileJson["functionality"]:
            self.functionality = tileJson["functionality"][type]
        else:
            self.functionality = None
    
    
    def loadTex(self, type, consts, tileJson):
        path = tileJson["imgs"][type]
        
        # Loads texture into class variable if it hasn't already been loaded
        if type not in self.textures:
            self.textures[path] = pygame.image.load(path)
    
    
    def render(self, window): # window is the Window object
        window.render(self.textures[self.type], self.pos)