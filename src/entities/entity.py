import pygame
import logging

import src.utility.utility as util
from src.utility.animation import Animation
from src.utility.vector import Vect
from src.ui.error import Error

class Entity:
    """ Towers and Enemies inherit from this class.
        Contains spritesheet/animations and rendering """

    spritesheets = {} # {path: animSpritesheet}

    def __init__(self, animData, pos = Vect(0, 0)):
        """ Loads spritesheet, animation, and creates self.pos
            animData parameter should be a dict with keys "path", "frames", and "delay" """
        self.log = logging.getLogger(__name__)
        
        self.pos = pos

        try:
            self.loadSpritesheet(animData["path"])
            self.loadAnim(animData)
        
        except KeyError as exc:
            Error.createError("Missing the following animation data for an entity.", self.log, exc)

    
    def loadSpritesheet(self, path):
        """ Load spritesheet image if it was not previous loaded """
        if path not in self.spritesheets:
            self.log.info(f"Loading entity spritesheet at {path}")
            self.spritesheets[path] = util.loadTexTransparent(path)
    
    def loadAnim(self, animData):
        """ Creates animation object """
        self.anim = Animation(self.spritesheets[animData["path"]], 
                              animData["frames"], animData["delay"])


    def updateAnim(self, window):
        """ Updates animation """
        self.anim.update(window)
    
    
    def render(self, window, xOffset=0, yOffset=0):
        """ Render animation at position """
        self.anim.render(window, self.pos + Vect(xOffset, yOffset))
    
    
    def getAnim(self): return self.anim

    def setPos(self, pos): self.pos = pos
    def addToPos(self, x): self.pos += x
    def getPos(self): return self.pos