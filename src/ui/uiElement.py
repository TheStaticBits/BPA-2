import pygame
import logging

from src.utility.vector import Vect
import src.utility.utility as util

class UIElement:
    """ Button and text objects inhert from UIElement. 
        Handles position, rendering, image data, and basic getters/setters """

    imageStorage = {}

    def __init__(self, pos, offset, centered, imgPath=None):
        self.log = logging.getLogger(__name__)
        
        self.uiOffset = offset
        self.pos = Vect(pos) + offset

        # Whether or not it should be centered at the position
        self.centered = centered 

        if imgPath != None:
            self.setImg(self.loadImg(imgPath))
        else:
            self.img = None
            self.size = None

        self.displaying = True


    def loadImg(self, path):
        """ Finds the image in the static dictionary (self.imageStorage) or loads it
            if it doesn't already exist and adds it to the dictionary """
        
        if path in self.imageStorage:
            return self.imageStorage[path]
        else:
            img = util.loadTexTransparent(path)
            self.imageStorage[path] = img
            return img

    
    def render(self, window, img=None):
        """ Renders the element with a different image if provided """
        if not self.displaying: return False

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
    def getCentered(self): return self.centered

    # Setters
    def addToPos(self, vect): self.pos += vect
    def setPos(self, vect): self.pos = vect
    def setDisplaying(self, display): self.displaying = display
    def setImg(self, img):
        self.img = img
        self.size = Vect(self.img.get_size())
    
    def setUIOffset(self, newOffset):
        """ Changing the offset of the position """
        self.pos -= self.uiOffset # Undoing original offset
        self.pos += newOffset # Adding new offset
        self.uiOffset = newOffset