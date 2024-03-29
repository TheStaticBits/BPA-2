import pygame
import logging

from src.ui.ui import UI
from src.utility.advDict import AdvDict
from src.ui.error import Error

class UpgradeMenu(UI):
    """ Class handling the tower upgrade menu
        inherits UI handling functionality from the UI class in ui.py """
    
    def __init__(self, consts, uiData):
        super().__init__(False, __name__)

        super().load(consts, "upgrades", uiData) # Loading UI objects for specifically the upgrades menu

        self.bought = False
        self.tower = None
        self.displayPrice = True
        self.sell = False
        self.sellPrice = None

        try:
            self.sellMultiplier = consts["game"]["sellMultiplier"]
        except KeyError as exc:
            Error.createError("Unable to find sell price multiplier in constants JSON.", self.log, exc)
    

    def format(self, stats):
        """ Takes in tower stats dictionary and formats it for display """
        return { "RANG": int(stats["range"] / 10),
                 "DMG": self.roundIfInt(stats["damage"]),
                 "SPD": int(10 / stats["attackCooldown"]) }
    

    def setPriceVisible(self, bool):
        """ Sets tower price to visible or not """
        self.displayPrice = bool
        # Setting images and text for cost displaying
        for resource in self.tower.getCurrentCosts().keys():
            super().getObj(resource + "Img").setDisplaying(bool)
            super().getObj(resource + "Cost").setDisplaying(bool)
    

    def calculateSellPrice(self, tower):
        """ Finds buy price and then updates the tower sell price to the purchasing price multiplied by the value in constants.json """
        # Original price is the first index in upgrade costs
        originalPrice = AdvDict(tower.getUpgradeInfo()[0]["costs"])
        self.sellPrice = originalPrice.copy()
        self.sellPrice *= self.sellMultiplier
        self.sellPrice.int()
    

    def roundIfInt(self, num):
        """ Removes decimal point if it ends in .0 """
        if num % 1 == 0: # Ends in .0
            return int(num)
        else:
            return num


    def selectTower(self, tower, index):
        """ Chooses a tower to show the upgrade menu for """

        self.log.info(f"Loaded upgrade menu for tower {tower.getType()}")

        super().setDisplaying(True)
        self.tower = tower
        self.towerIndex = index
        
        # Updating UI elements
        super().getObj("towerName").setText(tower.getType())
        super().getObj("upgradeLevel").setText(f"Level: {tower.getLevel() + 1}")

        towerStats = self.format(tower.getCurrentStats())
        # Iterates through all tower statistics and turns it into a list of each text row
        towerStatsStr = [ f"{key}: {value}" for key, value in towerStats.items() ]

        # If the tower has another level to upgrade to
        if len(tower.getUpgradeInfo()) - 1 > tower.getLevel():
            self.setPriceVisible(True)
            super().getObj("maxLevelText").setDisplaying(False)

            newTowerStats = self.format(tower.getUpgradeInfo()[tower.getLevel() + 1]["stats"])

            # Find difference between current stats and stats of a level above
            diff = {}
            for key in towerStats.keys():
                diff[key] = newTowerStats[key] - towerStats[key]

            # Add difference to the end of the stats displayed
            for index, key in enumerate(diff.keys()):
                towerStatsStr[index] += f" + {self.roundIfInt(diff[key])}"

        else: # Max level
            self.setPriceVisible(False)
            super().getObj("maxLevelText").setDisplaying(True)
            super().getObj("upgrade").setDisabled(True)
        
        super().getObj("towerStats").setText("\n".join(towerStatsStr))
        super().getObj("tower").setImg(tower.getImg())

        self.calculateSellPrice(tower)
    

    def getUpgradeCost(self):
        """ Returns cost to upgrade the tower (the cost of the tower level + 1) """
        return AdvDict(self.tower.getUpgradeInfo()[self.tower.getLevel() + 1]["costs"])
    

    def updatePrice(self, resources):
        """ Changes costs displayed and colors """
        if not self.displayPrice: return False

        price = self.getUpgradeCost()
        for resource, amount in resources.items():
            text = super().getObj(resource + "Cost")
            text.setText(str(price[resource]))

            if amount < price[resource]: 
                text.changeColor([ 220, 0, 0 ])
            else: 
                text.changeColor([ 0, 0, 0 ])
    

    def update(self, window, resources):
        """ Updates buttons and prices on upgrade screen"""
        super().update(window)
        if not super().isDisplaying(): return None
            
        self.updatePrice(resources)
        self.updateUpgrade(resources)
        self.updateSell()


    def updateUpgrade(self, playerResources):
        """ Updates the "Upgrade" button, testing if it's pressed when the player can buy it """
        if self.displayPrice and playerResources >= self.getUpgradeCost():
            super().getObj("upgrade").setDisabled(False)
            
            self.bought = False

            if super().getObj("upgrade").getPressed():
                self.tower.upgrade()
                self.selectTower(self.tower, self.towerIndex)
                self.bought = True

        else:
            super().getObj("upgrade").setDisabled(True)
            self.bought = False
    

    def updateSell(self):
        if super().getObj("sell").getPressed():
            self.sell = True
            self.tower.removeFromTile()
            super().setDisplaying(False)
    
    
    def getBought(self): return self.bought
    def getTower(self): return self.tower

    def isSold(self): return self.sell
    def getSellPrice(self): return self.sellPrice
    def getTowerIndex(self): return self.towerIndex
    def setSold(self, val): self.sell = val