import pygame
import logging

from src.ui.ui import UI

class UpgradeMenu(UI):
    """ Class handling the tower upgrade menu
        inherits UI handling functionality from the UI class in ui.py """
    
    def __init__(self, consts, uiData):
        super().__init__(True, __name__)

        super().load(consts, "upgrades", uiData) # Loading UI objects for specifically the upgrades menu