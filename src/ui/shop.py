import pygame
import logging

from src.ui.ui import UI
from src.ui.button import Button
from src.utility.animation import Animation
from src.ui.error import Error

class Shop(UI):
    """ Inherits from UI class for handling objects on the UI and more. 
        This class handles the functionality of the shop UI specifically. """
    
    towerImages = {} # Stores all tower images for the UI

    def __init__(self, consts, uiData, towerData):
        super().__init__(True, __name__)

        super().load(consts, "shop", uiData) # Loading UI objects from the UI data in the JSON file
        
        self.towerData = towerData
        if self.towerImages != {}: # if it has not already been loaded
            self.loadTowerImages()
        
        self.towerSelected = 0 # First tower
        self.canBuy = False
        self.bought = False

        self.updateTowerMenu()
    
    
    def loadTowerImages(self):
        """ Loading the first frame of the tower images for the shop menu """
        for name, data in self.towerData.items():
            anim = data["animation"]

            # Load animation
            try:
                temp = Animation(anim["path"], anim["frames"], anim["delay"])
            except KeyError as exc:
                Error.createError(f"Unable to find some animation data for the tower {name}.", self.log, exc)

            self.towerImages[name] = temp.getFrame(0) # Gets first frame of tower animation
    

    def updateTowerMenu(self):
        """ Updates tower elements on screen for a new selected tower """
        towerName = self.getSelectedTowerName()

        # Change tower image
        super().getObj("tower").setImg(self.towerImages[towerName])
        # Change tower name
        super().getObj("towerName").changeText(towerName)
    

    def updateButtons(self):
        """ Updates tower scrolling """
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
    

    def updateResources(self, resources):
        """ Updates amount of resources displayed """
        for name, amount in resources.items():
            obj = super().getObj(name + "Amount")
            obj.changeText(str(amount))
    

    def updateTowerCosts(self, resources):
        """ Updates the costs of the towers, changing text colors as well """
        prices = self.getTowerPrice()

        self.canBuy = True

        for name, amount in resources.items():
            text = super().getObj(name + "Cost")

            if prices[name] == 0:
                # Don't render those parts when that resource's price is zero
                super().getObj(name + "Img").setDisplaying(False)
                super().getObj(name + "Cost").setDisplaying(False)
            
            else:
                super().getObj(name + "Img").setDisplaying(True)
                super().getObj(name + "Cost").setDisplaying(True)

                text.changeText(str(prices[name]))
                
                if amount < prices[name]:
                    text.changeColor([ 255, 0, 0 ]) # Set to red color
                    self.canBuy = False
                else:
                    text.changeColor([ 0, 0, 0 ]) # Set to black (has enough to buy it)


    def update(self, window, resources):
        """ Updates everything within the shop menu """
        super().update(window)

        self.updateResources(resources)
        self.updateButtons()
        self.updateTowerCosts(resources)

        # Test for player buying a tower
        self.bought = False
        if super().getObj("buy").getPressed():
            if self.canBuy:
                self.bought = True

    
    def getSelectedTowerName(self):
        """ Gets the name of the tower at the index of the currently selected tower """
        return list(self.towerData.keys())[self.towerSelected]
    
    def getTowerPrice(self):
        """ Gets the first upgrade cost, the initial cost, of the tower """
        try:
            return self.towerData[self.getSelectedTowerName()]["upgrades"][0]["costs"]
        except KeyError as exc:
            Error.createError(f"Unable to find the cost of the selected tower in the shop, {self.getSelectedTowerName()}.", self.log, exc)
    

    def getBought(self): return self.bought