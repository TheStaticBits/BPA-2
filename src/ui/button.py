import pygame
import logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.ui.uiElement import UIElement
import src.ui.error as error

class Button(UIElement):
    """ Button object for the UI, inherits from UIElement """
    
    def __init__(self, name, buttonData, offset, text=None):
        """ Initializes the button from the given button name and button data JSONs. """
        self.log = logging.getLogger(__name__)

        self.pressed = False
        self.text = text

        # Loading button data from the JSON file, along with catching any potential errors
        try:
            self.offsets = buttonData["offsets"]
            pos = buttonData["pos"]
            path = buttonData["path"]

            if self.text != None:
                # Height of the shadowed area of the button image
                # Only needed for centering the text
                self.chinHeight = buttonData["chinHeight"]

        except KeyError as exc:
            error.Error.createError(f"Unable to find the following data within the {name} button's data.",
                              self.log, exc)
            return None
            

        try:
            centered = buttonData["centered"]
        except KeyError as exc:
            error.Error.createError(f"Unable to find the data for \"centered\" for the {name} button. Defaulting to False.", 
                              self.log, exc, recoverable=True)
            centered = False


        super().__init__(pos, offset, centered, imgPath=path)

        self.heightOffset = self.offsets["default"]
        self.moveToOffset = 0
    

    def centerText(self):
        """ Centers the text object on the button """

        if self.text == None: return None

        size = super().getSize()

        textPos = super().getPos().copy()
        # Centers text on the upper part of the button
        textPos += Vect(size.x, size.y - self.chinHeight) / 2
        textPos -= self.text.getSize() / 2

        textPos.y += self.heightOffset

        self.text.setPos(textPos)


    def update(self, window):
        """ Updates the button hover based on the mouse position, etc. """
        # if not displaying, don't update anything and break out of the function
        if not super().getDisplaying(): return None

        self.pressed = False

        if util.pointRectCollision(window.getMousePos(), super().getPos(), super().getSize()):
            if window.getMouse("left"):
                self.moveToOffset = self.offsets["pressed"] # Moves down
            elif window.getMouseReleased("left"):
                self.pressed = True
                self.log.info(f"Pressed button")
            else:
                self.moveToOffset = 0 # Moves all the way to the top
        
        else:
            self.moveToOffset = self.offsets["default"]
        
        # Moves the y position slowly to the offset
        self.heightOffset += (self.moveToOffset - self.heightOffset) * window.getDeltaTime() * self.offsets["moveSpeed"]

        self.centerText()
    

    def renderText(self, window):
        """ Renders button text if there is any """
        if self.text != None:
            self.text.render(window)


    def render(self, window):
        """ Cuts off the bottom of the button when at an offset and renders it """
        if not super().getDisplaying(): False

        if self.heightOffset != 0:
            img = pygame.Surface(super().getSize().getTuple(), 
                                 flags=pygame.SRCALPHA)
            img.blit(super().getImg(), (0, self.heightOffset))

        else:
            img = super().getImg()
        
        super().render(window, img=img)
        self.renderText(window)
    

    def getPressed(self): return self.pressed
    def getTextObj(self): return self.text