import pygame
import logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.ui.uiElement import UIElement

class Button(UIElement):
    """ Button object for the UI, inherits from UIElement """
    
    def __init__(self, buttonName, buttonData, offset, text=None):
        """ Initializes the button from the given button name and button data JSONs. """
        self.log = logging.getLogger(__name__)

        self.offsets = buttonData["offsets"]
        super().__init__(buttonName, buttonData["pos"], offset, buttonData["path"])

        self.heightOffset = 0
        self.moveToOffset = 0

        self.pressed = False
        self.text = text
    

    def centerText(self):
        """ Centers the text object on the button """

        if self.text == None: return None

        size = super().getSize()

        textPos = super().getPos().copy()
        # Centers text on the upper part of the button
        textPos += Vect(size.x, size.y - self.offsets["pressed"]) / 2
        textPos -= self.text.getSize() / 2

        textPos.y += self.heightOffset

        self.text.setPos(textPos)


    def update(self, window):
        """ Updates the button hover based on the mouse position, etc. """
        self.pressed = False

        if util.pointRectCollision(window.getMousePos(), super().getPos(), super().getSize()):
            if window.getMouse("left"):
                self.heightOffset = self.offsets["pressed"] # Moves down
            elif window.getMouseReleased("left"):
                self.pressed = True
            else:
                self.heightOffset = 0 # Moves all the way to the top
        
        else:
            self.heightOffset = self.offsets["default"]
        
        # Moves the y position slowly to the offset
        super().addToPos((self.heightOffset - super().getPos().y) * window.getDeltaTime() * self.offsets["moveSpeed"])

        self.centerText()
    

    def renderText(self, window):
        """ Renders button text if there is any """
        if self.text != None:
            self.text.render(window)


    def render(self, window):
        """ Cuts off the bottom of the button when at an offset and renders it """ 
        if self.heightOffset != 0:
            img = pygame.Surface(super().getSize().getTuple(), 
                                 flags=pygame.SRCALPHA)
            img.blit(super().getImg(), (0, self.heightOffset))

        else:
            img = super().getImg()
        
        super().render(window, img=img)
        self.renderText(window)
    

    def getPressed(self): return self.pressed