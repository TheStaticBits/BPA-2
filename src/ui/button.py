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
        self.disabled = False

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
    

    def updateMovement(self, window):
        """ Updates button animation and button press detection"""
        # Test if the mouse is not near the button, hovering over it, or clicking it
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

        # Only for when the deltaTime is very high, when the game freezes for a bit or more,
        # cap it at the max offset
        if self.heightOffset < 0:
            self.heightOffset = 0


    def update(self, window):
        """ Updates the button hover based on the mouse position, etc. """
        # if not displaying, don't update anything and break out of the function
        if not super().getDisplaying(): 
            return None

        self.pressed = False

        if not self.disabled: # Update the button normally with movement etc.
            self.updateMovement(window)
        
        else: # Button is disabled, so don't update mouse collisions, animation, etc.
            self.heightOffset = self.offsets["default"] # Default offset

        # In case the text was updated, center its position on the button
        self.centerText()
    

    def renderText(self, window):
        """ Renders button text if there is any """
        if self.text != None:
            self.text.render(window)


    def render(self, window):
        """ Cuts off the bottom of the button when at an offset and renders it """
        if not super().getDisplaying(): 
            # Makes button not visible when button is invisible
            if self.text != None:
                self.text.setDisplaying(False) # Set the text displaying as the same as the button

            return False # Do not render the button or text, exit the function

        else:
            if self.text != None:
                self.text.setDisplaying(True)
        

        if self.heightOffset != 0:
            img = pygame.Surface(super().getSize().getTuple(), 
                                 flags=pygame.SRCALPHA)
            img.blit(super().getImg(), (0, self.heightOffset))
            # Any part of the button below its bottom will be cut off because the button
            # is being drawn on another surface with the same size as the button

        else:
            img = super().getImg().copy()
        
        if self.disabled: # Gray out the button since it is disabled
            graySurf = pygame.Surface(img.get_size()) # Same size as the button image
            graySurf.fill((150, 150, 150)) # Fill with a gray
            graySurf.set_alpha(150) # Set alpha to 150/255
            img.blit(graySurf, (0, self.heightOffset)) # Fill the button part with gray
        
        super().render(window, img=img)
        self.renderText(window)


    def getPressed(self): return self.pressed
    def getTextObj(self): return self.text

    def setDisabled(self, bool): self.disabled = bool