import pygame
import logging

from src.button import Button

class UI:
    def __init__(self, display): 
        self.log = logging.getLogger(__name__)

        self.objects = []
        self.displaying = display
    
    def load(self, type, data):
        """ Loads all objects """
        self.data = data[type]

        for buttonName, buttonData in self.data["buttons"].items():
            self.objects.append(Button(buttonName, buttonData))