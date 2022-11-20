import pygame
import logging

from src.utility.vector import Vect
import src.utility.utility as util

class UIElement:
    def __init__(self, name, pos, imgPath=None):
        self.log = logging.getLogger(__name__)
        
        self.name = name
        self.pos = Vect(pos)

        if imgPath != None:
            self.setImg(util.loadTex(imgPath))
        else:
            self.img = None
            self.size = None

    
    def render(self, window, offset, img=None):
        """ Renders the element with a different image if provided """
        
        if img == None:
            window.render(self.img, self.pos + offset)
        else:
            window.render(img, self.pos + offset)
    
    
    def update(self, window):
        # Overriden in subclasses
        pass
        
        
    # Getters
    def getSize(self): return self.size
    def getImg(self): return self.img
    def getPos(self): return self.pos
    def getName(self): return self.name

    # Setters
    def addToPos(self, vect): self.pos += vect
    def setImg(self, img):
        self.img = img
        self.size = Vect(self.img.get_size())