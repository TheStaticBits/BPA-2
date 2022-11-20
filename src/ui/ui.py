import pygame
import logging

from src.ui.uiElement import UIElement
from src.ui.button import Button
from src.ui.text import Text
from src.utility.vector import Vect

class UI:
    """ Object for more specific UI interfaces to inherit from to handle buttons, etc. """
    def __init__(self, display): 
        self.log = logging.getLogger(__name__)

        self.objects = {}
        self.displaying = display
    

    def load(self, consts, type, data):
        """ Loads all UI objects """
        self.data = data[type]
        self.offset = Vect(self.data["offset"])

        # Loading all static images
        for name, imgData in self.data["images"].items():
            self.objects[name] = UIElement(imgData["pos"], self.offset, imgData["centered"], imgPath=imgData["path"])
        
        # Loading text objects
        for name, textData in self.data["text"].items():
            self.objects[name] = Text(textData, consts, self.offset)

        # Loading button objects (may use text objects from above)
        for name, buttonData in self.data["buttons"].items():
            text = None
            if "text" in buttonData: # Button has text on it
                # Find matching text object in already loaded text objects
                text = self.getObj(buttonData["text"])
                self.objects.pop(buttonData["text"])

            self.objects[name] = Button(buttonData, self.offset, text)
    

    def update(self, window):
        """ Updates the UI objects """
        for obj in self.objects.values():
            obj.update(window)


    def render(self, window):
        """ Renders the UI objects """
        for obj in self.objects.values():
            obj.render(window)


    def getObj(self, name): return self.objects[name]