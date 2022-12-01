import pygame
import logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.ui.uiElement import UIElement
from src.ui.error import Error

class Text(UIElement):
    """ Handles a piece of text on a UI, its position, rendering, etc. """

    # Static variable containing all pygame.font.Font objects of different font sizes
    fonts = {}

    def __init__(self, name, type, textData, consts, offset):
        """ Loads the text data, Pygame font object, and the text image """
        self.log = logging.getLogger(__name__)

        if "pos" in textData:
            pos = textData["pos"]
            
            try:
                centered = textData["centered"]

            except KeyError as exc:
                Error.createError(f"Unable to find \"centered\" data for the {name} text object, defaulting to False", 
                                  self.log, exc, recoverable=True)
                centered = False
            
        else:
            pos = Vect(0, 0)
            centered = False

        super().__init__(pos, offset, centered)

        try:
            self.text = textData["text"]
            self.fontSize = textData["fontSize"]
            self.color = textData["color"]
        
        except KeyError as exc:
            Error.createError("Unable to find required data to load the {type} text object.", self.log, exc)
            return None


        if self.fontSize not in self.fonts: 
            try:
                self.fonts[self.fontSize] = pygame.font.Font(consts["miscPaths"]["font"], self.fontSize)

            except KeyError as exc:
                Error.createError("Unable to find and load font path from constants file.", self.log, exc)

        if "lineSpacing" in textData:
            self.lineSpacing = textData["lineSpacing"]

            # Finds the height of a character in the font
            self.charHeight = util.renderFont(".", self.fonts[self.fontSize], self.color).get_height()
        
        self.updateTextImg()


    def changeText(self, text):
        """ Changes text and text image """
        if self.text != text:
            self.text = text
            self.updateTextImg()


    def changeColor(self, color):
        """ Changes color and text image"""
        if self.color != color:
            self.color = color
            self.updateTextImg()

    
    def updateTextImg(self):
        """ Updates the text image """
        self.hasNewLines = "\n" in self.text

        if not self.hasNewLines:
            super().setImg(util.renderFont(self.text, self.fonts[self.fontSize], self.color))

        else: # Handling newlines in the text (Pygame does not automatically handle them)
            lineImages = []
            text = self.text.split("\n")
            widestLineSize = 0
            
            # Getting the images for each line of text and finding the widest line and its size
            for line in text:
                lineImage = util.renderFont(line, self.fonts[self.fontSize], self.color)
                lineImages.append(lineImage)
                
                if lineImage.get_width() > widestLineSize:
                    widestLineSize = lineImage.get_width()
            
            # Creates one image for the entire textbox with the size of all lines lined up and a width
            # of the longest line in the text box.
            image = pygame.Surface((widestLineSize, len(lineImages) * (self.charHeight + self.lineSpacing)), 
                                   flags=pygame.SRCALPHA)
            
            # Rendering text to the textbox image
            for lineNum, lineImg in enumerate(lineImages):

                # If the object is centered, also center the text
                if super().getCentered():
                    # Centered x offset for the text inside the textbox image
                    x = (image.get_width() + lineImg.get_width()) // 2
                else: 
                    x = 0

                image.blit(lineImg, ( x, lineNum * (self.charHeight + self.lineSpacing) ))

            super().setImg(image)
    
    
    def getColor(self): return self.color