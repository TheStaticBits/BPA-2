import pygame
import logging

from src.utility.vector import Vect
import src.utility.utility as util

class UIElement:
    def __init__(self, name, pos, offset, centered, imgPath=None):
        self.log = logging.getLogger(__name__)
        
        self.name = name
        self.pos = Vect(pos) + offset
        # Whether or not it should be centered at the position
        self.centered = centered 

        if imgPath != None:
            self.setImg(util.loadTex(imgPath))
        else:
            self.img = None
            self.size = None

    
    def render(self, window, img=None):
        """ Renders the element with a different image if provided """
        if img == None:
            window.render(self.img, self.getPos())
        else:
            window.render(img, self.getPos())
    
    
    def update(self, window):
        # Overriden in subclasses
        pass


    def getPos(self):
        """ Accounts for whether the UI element centered as well """
        if self.centered:
            return self.pos - (self.getSize() / 2)
        else:
            return self.pos
        
        
    # Getters
    def getSize(self): return self.size
    def getImg(self): return self.img
    def getName(self): return self.name

    # Setters
    def addToPos(self, vect): self.pos += vect
    def setPos(self, vect): self.pos = vect
    def setImg(self, img):
        self.img = img
        self.size = Vect(self.img.get_size())