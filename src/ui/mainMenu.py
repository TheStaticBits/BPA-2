import pygame
import logging

from src.ui.ui import UI

class MainMenu(UI):
    def __init__(self, consts, uiData):
        super().__init__(True, __name__)
        
        super().load(consts, "mainMenu", uiData) # Loading UI objects for specifically the upgrades menu