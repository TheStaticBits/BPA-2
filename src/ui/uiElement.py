import pygame
import logging

class UIElement:
    def __init_(self, pos, imgPath):
        self.log = logging.getLogger(__name__)
        
        self.pos = Vect(pos)
        self.img = util.loadTex(imgPath)