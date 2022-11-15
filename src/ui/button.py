import pygame
import logging

import utility as util
from vector import Vect

class Button:
    """ Button """
    def __init__(self, pos, buttonName, buttonData):
        """ Initializes the button from the given button name and button data JSONs. """
        self.log = logging.getLogger(__name__)

        data = buttonData[buttonName]
        self.pos = pos
        self.pxHeight = data["height"]
        self.offsets = data["offsets"]

        self.img = util.loadTex(data["path"])
        self.size = Vect(self.image.get_size())

        self.heightOffset = 0
        self.moveToOffset = 0

        self.pressed = False

    def update(self, window):
        """ Updates the button hover based on the mouse position, etc. """
        self.pressed = False

        if util.pointRectCollision(window.getMousePos(), self.pos, self.size):
            if window.getMouse("left"):
                self.heightOffset = self.offsets["pressed"] # Moves down
            elif window.getMouseReleased("left"):
                self.pressed = True
            else:
                self.heightOffset = 0 # Moves all the way to the top
        
        else:
            self.heightOffset = self.offsets["default"]
        
        # Moves the y position slowly to the offset
        self.pos.y += (self.heightOffset - self.pos.y) * window.getDeltaTime() * self.offsets["moveSpeed"]

    def render(self, window):
        """ Cuts off the bottom of the button when at an offset and renders it """ 
        if self.heightOffset != 0:
            img = pygame.Surface(self.size.getTuple())
            img.blit(self.img, (0, self.heightOffset))
        else:
            img = self.img
        
        window.render(img, self.pos)