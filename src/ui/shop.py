import pygame
import logging

from src.ui.ui import UI
from src.ui.button import Button
from src.utility.animation import Animation

class Shop(UI):
    """ Inherits from UI class for handling objects on the UI and more. 
        This class handles the functionality of the shop UI specifically. """

    def __init__(self, consts, uiData, towerData):
        super().__init__(True)

        super().load(consts, "shop", uiData)
        
        self.towerData = towerData
        self.towerImages = {}

        # Loading towers for the shop menu
        for name, data in self.towerData.items():
            anim = data["animation"]
            temp = Animation(anim["path"], anim["frames"], anim["delay"])

            self.towerImages[name] = temp.getFrame(0) # Gets first frame of tower animation
        
        self.towerSelected = 0 # First tower

        self.updateTowerMenu()
    

    def updateTowerMenu(self):
        """ Updates tower elements on screen for a new selected tower """
        # Gets the name of the tower at the index of the currently selected tower
        towerName = list(self.towerData.keys())[self.towerSelected]

        # Change tower image
        super().getObj("tower").setImg(self.towerImages[towerName])
        # Change tower name
        super().getObj("towerName").changeText(towerName)


    def update(self, window, resources):
        """ Handles button events and shop-related updates """
        super().update(window)


        # Updates amount of resources displayed
        for name, amount in resources.items():
            obj = super().getObj(name + "Txt")
            obj.changeText(str(amount))
        

        # Updates tower scrolling
        if super().getObj("left").getPressed(): # Left button
            self.towerSelected -= 1 # Decrement
            if self.towerSelected < 0:
                self.towerSelected = len(self.towerData) - 1
            self.updateTowerMenu()

        elif super().getObj("right").getPressed(): # Right button
            self.towerSelected += 1 # Increment
            if self.towerSelected >= len(self.towerData):
                self.towerSelected = 0
            self.updateTowerMenu()

    
    def render(self, window):
        """ Handles shop-specific rendering events """
        super().render(window)