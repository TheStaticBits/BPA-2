import pygame
import logging

from src.ui.button import Button
from src.ui.text import Text
from src.utility.vector import Vect

class UI:
    """ Object for more specific UI interfaces to inherit from to handle buttons, etc. """
    def __init__(self, display): 
        self.log = logging.getLogger(__name__)

        self.objects = []
        self.displaying = display
    

    def load(self, consts, type, data):
        """ Loads all UI objects """
        self.data = data[type]
        self.offset = Vect(self.data["offset"])

        for textName, textData in self.data["text"].items():
            self.objects.append(Text(textName, textData, consts, self.offset))

        for buttonName, buttonData in self.data["buttons"].items():
            
            text = None
            if "text" in buttonData: # Button has text on it
                # Find matching text object in already loaded text objects
                for obj in self.objects:
                    if obj.getName() == buttonData["text"]:
                        text = obj
                    
                        self.objects.remove(obj)
                        break

            self.objects.append(Button(buttonName, buttonData, self.offset, text))
    

    def update(self, window):
        """ Updates the UI objects """
        for obj in self.objects:
            obj.update(window)


    def render(self, window):
        """ Renders the UI objects """
        for obj in self.objects:
            obj.render(window)