import pygame
import logging

from src.ui.ui import UI
from src.ui.button import Button
from src.ui.error import Error
from src.utility.animation import Animation
from src.utility.advDict import AdvDict

class Shop(UI):
    """ Inherits from UI class for handling objects on the UI and more. 
        This class handles the functionality of the shop UI specifically. """
    
    towerImages = {} # Stores all tower images for the UI

    def __init__(self, consts, uiData, towerData):
        super().__init__(True, __name__)

        super().load(consts, "shop", uiData) # Loading UI objects from the UI data in the JSON file
        
        self.towerData = towerData
        if len(self.towerImages) == 0: # if it has not already been loaded
            self.loadTowerImages()
        
        self.towerSelected = 0 # First tower
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
        super().getObj("towerName").setText(towerName)

        self.towerPrice = AdvDict(self.getTowerPrice())
    

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
            obj.setText(str(amount))
    

    def updateTowerCosts(self, resources):
        """ Updates the costs of the towers, changing text colors as well """
        for resource, amount in resources.items():
            text = super().getObj(resource + "Cost")

            text.setText(str(self.towerPrice[resource]))
            
            if amount < self.towerPrice[resource]:
                text.changeColor([ 220, 0, 0 ]) # Set to red color
            else:
                text.changeColor([ 0, 0, 0 ]) # Set to black (has enough to buy it)


    def update(self, window, resources, showingUpgrades, isPlacingTower, wavesHandler, tileset):
        """ Updates everything within the shop menu """
        
        # If the upgrades menu is not open, update shop buttons
        if not showingUpgrades:
            super().update(window)
            self.updateButtons()

        self.updateResources(resources)
        self.updateTowerCosts(resources)

        if not isPlacingTower and resources >= self.towerPrice:
            if tileset.hasAvailableTile(): # If at least one tile doesn't have a tower 
                super().getObj("buy").setDisabled(False)

                # Test for player buying a tower
                self.bought = False
                if super().getObj("buy").getPressed():
                    self.bought = True

        else:
            super().getObj("buy").setDisabled(True)
            self.bought = False
        
        # Updates stats for wave number and player health on screen
        super().getObj("waveNum").setText(f"Wave: {wavesHandler.getWaveNum() + 1}")
        super().getObj("playerHealth").setText(f"HP: {wavesHandler.getPlayerHealth()}")

        # Sets skip button to be disabled if it isn't currently between waves
        super().getObj("skip").setDisabled(not wavesHandler.isBetweenWaves())

    
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

    def pauseButtonPressed(self): 
        return super().getObj("pause").getPressed()
    
    def skipButtonPressed(self):
        return super().getObj("skip").getPressed()