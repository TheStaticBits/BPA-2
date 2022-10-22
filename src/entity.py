import pygame
import logging

import src.utility as util
import src.animation as anim

class Entity:
    """ Towers and Enemies inherit from this class.
        Contains spritesheet/animations and rendering """

    spritesheets = {} # {path: animSpritesheet}

    def __init__(self, type, path):
        self.loadSpritesheet(path)

        self.anim = anim.Animation(self.spritesheets[path], )

    
    def loadSpritesheet(self, path):
        if path not in self.spritesheets:
            self.spritesheets[path] = util.loadTexTransparent(path)