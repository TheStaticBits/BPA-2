import pygame
import logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.ui.uiElement import UIElement

class Text(UIElement):
    """ Handles a piece of text on a UI, its position, rendering, etc. """

    # Static variable containing all pygame.font.Font objects of different font sizes
    fonts = {}

    def __init__(self, textData, consts, offset):
        """ Loads the text data, Pygame font object, and the text image """
        self.log = logging.getLogger(__name__)

        if "pos" in textData:
            pos = textData["pos"]
            centered = textData["centered"]
        else:
            pos = Vect(0, 0)
            centered = False

        super().__init__(pos, offset, centered)

        self.text = textData["text"]
        self.fontSize = textData["fontSize"]
        self.color = textData["color"]

        if self.fontSize not in self.fonts: 
            self.fonts[self.fontSize] = pygame.font.Font(consts["miscPaths"]["font"], self.fontSize)
        
        self.updateTextImg()


    def changeText(self, text):
        self.text = text
        self.updateTextImg()
    
    def updateTextImg(self):
        """ Updates the text image """
        super().setImg(util.renderFont(self.text, self.fonts[self.fontSize], self.color))