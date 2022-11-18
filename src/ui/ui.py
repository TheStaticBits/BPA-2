import pygame
import logging

from src.ui.button import Button

class UI:
    """ Object for more specific UI interfaces to inherit from to handle buttons, etc. """
    def __init__(self, display): 
        self.log = logging.getLogger(__name__)

        self.objects = []
        self.displaying = display
    

    def load(self, type, data):
        """ Loads all UI objects """
        self.data = data[type]

        for buttonName, buttonData in self.data["buttons"].items():
            self.objects.append(Button(buttonName, buttonData))
    

    def update(self, window):
        """ Updates the UI objects """
        for obj in self.objects:
            obj.update(window)


    def render(self, window):
        """ Renders the UI objects """
        for obj in self.objects:
            obj.render(window)