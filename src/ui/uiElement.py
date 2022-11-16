import pygame
import logging

from src.utility.vector import Vect

class UIElement:
    def __init_(self, pos, imgPath):
        self.log = logging.getLogger(__name__)
        
        self.pos = Vect(pos)
        self.img = util.loadTex(imgPath)
        self.size = Vect(self.image.get_size())

    
    def render(self, window, img=None):
        """ Renders the element with a different image if provided """
        
        if img != None:
            window.render(self.img, self.pos)
        else:
            window.render(img, self.pos)
        
        
    # Getters
    def getSize(self): return self.size
    def getImg(self): return self.img
    def getPos(self): return self.pos

    # Setters
    def addToPos(self, vect): self.pos += vect