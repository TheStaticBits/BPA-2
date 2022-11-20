import pygame
import logging

from src.utility.vector import Vect
import src.utility.utility as util

class UIElement:
    def __init__(self, pos, offset, centered, imgPath=None):
        self.log = logging.getLogger(__name__)
        
        self.pos = Vect(pos) + offset
        # Whether or not it should be centered at the position
        self.centered = centered 

        if imgPath != None:
            self.setImg(util.loadTexTransparent(imgPath))
        else:
            self.img = None
            self.size = None

        self.displaying = True

    
    def render(self, window, img=None):
        """ Renders the element with a different image if provided """
        if not self.displaying: False

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
    def getDisplaying(self): return self.displaying

    # Setters
    def addToPos(self, vect): self.pos += vect
    def setPos(self, vect): self.pos = vect
    def setInvisible(self): self.displaying = False
    def setImg(self, img):
        self.img = img
        self.size = Vect(self.img.get_size())
    