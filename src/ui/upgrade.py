import pygame
import logging

from src.ui.ui import UI

class UpgradeMenu(UI):
    """ Class handling the tower upgrade menu
        inherits UI handling functionality from the UI class in ui.py """
    
    def __init__(self, consts, uiData):
        super().__init__(True, __name__)

        super().load(consts, "upgrades", uiData) # Loading UI objects for specifically the upgrades menu
        super().setDisplaying(False)
    

    def selectTower(self, tower):
        """ Chooses a tower to show the upgrade menu for """

        super().setDisplaying(True)
        
        # Change tower name displayed, upgrade level, image, price of upgrade, and upgrade stats here
        super().getObj("towerName").changeText(tower.getType())