import pygame
import logging

import src.window as window

class Texture:
    """ Renderable object """
    def __init__(self, path, x = 0, y = 0):
        """ Initialize texture and position """
        self.log = logging.getLogger(__name__)
        
        self.img = pygame.image.load(path)
        self.position = [x, y]


    def render(self, dest):
        """ Render texture to window at its position """
        self.img.blit(dest, self.getPos())


    # Getters
    def getPos(self): return self.position
    def getX(self):   return self.getPos[0]
    def getY(self):   return self.getPos[1]

    def getSize(self):   return self.img.get_size()
    def getWidth(self):  return self.getSize()[0]
    def getHeight(self): return self.getSize()[1]


    # Setters
    def setPos(self, x = None, y = None): 
        if (x != None): self.position[0] = x
        if (y != None): self.position[1] = y