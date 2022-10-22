import pygame
import logging

import src.utility as util
import src.animation as anim
from src.vector import Vect

class Entity:
    """ Towers and Enemies inherit from this class.
        Contains spritesheet/animations and rendering """

    spritesheets = {} # {path: animSpritesheet}

    def __init__(self, animData, pos = Vect(0, 0)):
        """ Loads spritesheet, animation, and creates self.pos
            animData parameter should be a dict with keys "path", "frames", and "delay" """
        self.log = logging.getLogger(__name__)

        self.loadSpritesheet(animData["path"])
        self.anim = anim.Animation(self.spritesheets[animData["path"]], 
                                   animData["frames"], animData["delay"])
        self.pos = pos

    
    def loadSpritesheet(self, path):
        """ Load spritesheet image if it was not previous loaded """
        if path not in self.spritesheets:
            self.log.info(f"Loading entity spritesheet at {path}")
            self.spritesheets[path] = util.loadTexTransparent(path)


    def updateAnim(self, window):
        """ Updates animation """
        self.anim.update(window)
    
    
    def render(self, window):
        """ Render animation at position """
        self.anim.render(window, self.pos)
    
    
    def getAnim(self): return self.anim

    def setPos(self, pos): self.pos = pos
    def getPos(self): return self.pos