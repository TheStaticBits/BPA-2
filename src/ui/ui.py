import pygame
import logging

from src.ui.uiElement import UIElement
from src.ui.button import Button
from src.ui.text import Text
from src.utility.vector import Vect
from src.ui.error import Error

class UI:
    """ Object for more specific UI interfaces to inherit from to handle buttons, etc. """
    def __init__(self, display, fileName): 
        self.log = logging.getLogger(fileName)

        self.objects = {}
        self.displaying = display
    

    def load(self, consts, type, data):
        """ Loads all UI objects """
        try:
            self.data = data[type]
            self.offset = Vect(self.data["offset"])

            # Loading all static images
            for name, imgData in self.data["images"].items():
                self.objects[name] = UIElement(imgData["pos"], self.offset, imgData["centered"], imgPath=imgData["path"])
            
            # Loading text objects
            for name, textData in self.data["text"].items():
                self.objects[name] = Text(name, textData, consts, self.offset)

            # Loading button objects (may use text objects from above)
            for name, buttonData in self.data["buttons"].items():
                text = None
                if "text" in buttonData: # Button has text on it
                    # Find matching text object in already loaded text objects
                    text = self.getObj(buttonData["text"])
                    self.objects.pop(buttonData["text"])

                self.objects[name] = Button(name, buttonData, self.offset, text)
        
        except KeyError as exc:
            Error.createError(f"Unable to find required data to load the UI {type}.", self.log, exc)
            

    def update(self, window):
        """ Updates the UI objects """
        if self.displaying:
            for obj in self.objects.values():
                obj.update(window)


    def render(self, window):
        """ Renders the UI objects """
        if self.displaying:
            for obj in self.objects.values():
                obj.render(window)


    def getObj(self, name): return self.objects[name]
    def getLogger(self): return self.log
    
    def setDisplaying(self, display): self.displaying = display