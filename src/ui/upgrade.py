import pygame
import logging

from src.ui.ui import UI
from src.utility.advDict import AdvDict

class UpgradeMenu(UI):
    """ Class handling the tower upgrade menu
        inherits UI handling functionality from the UI class in ui.py """
    
    def __init__(self, consts, uiData):
        super().__init__(True, __name__)

        super().load(consts, "upgrades", uiData) # Loading UI objects for specifically the upgrades menu
        super().setDisplaying(False)

        self.bought = False
        self.tower = None
        self.displayPrice = True
    

    def format(self, stats):
        """ Takes in tower stats dictionary and formats it for display """
        return { "RANG": int(stats["range"] / 10),
                 "DMG": stats["damage"],
                 "SPD": int(10 / stats["attackCooldown"]) }
    

    def setPriceVisible(self, bool):
        """ Sets tower price to visible or not """
        self.displayPrice = bool
        # Setting images and text for cost displaying
        for resource in self.tower.getCurrentCosts().keys():
            super().getObj(resource + "Img").setDisplaying(bool)
            super().getObj(resource + "Cost").setDisplaying(bool)
    

    def selectTower(self, tower):
        """ Chooses a tower to show the upgrade menu for """

        self.log.info(f"Loaded upgrade menu for tower {tower.getType()}")

        super().setDisplaying(True)
        self.tower = tower
        
        # Change tower name displayed, upgrade level, image, price of upgrade, and upgrade stats here
        super().getObj("towerName").changeText(tower.getType())
        super().getObj("upgradeLevel").changeText(f"Lvl: {tower.getLevel() + 1}")

        towerStats = self.format(tower.getCurrentStats())
        towerStatsStr = [f"{key}: {value}" for key, value in towerStats.items()]

        # If the tower has another level to upgrade to
        if len(tower.getUpgradeInfo()) - 1 > tower.getLevel():
            self.setPriceVisible(True)
            super().getObj("upgrade").setDisplaying(True)

            newTowerStats = self.format(tower.getUpgradeInfo()[tower.getLevel() + 1]["stats"])

            # Find difference between current stats and stats of a level above
            diff = {}
            for key in towerStats.keys():
                diff[key] = newTowerStats[key] - towerStats[key]

            # Add difference to the end of the stats displayed
            for index, key in enumerate(diff.keys()):
                towerStatsStr[index] += f" + {diff[key]}"

        else:
            self.setPriceVisible(False)
            super().getObj("upgrade").setDisplaying(False)
        
        super().getObj("towerStats").changeText("\n".join(towerStatsStr))
        
        super().getObj("tower").setImg(tower.getImg())
    

    def getUpgradeCost(self):
        """ Returns cost to upgrade the tower (the cost of the tower level + 1) """
        return AdvDict(self.tower.getUpgradeInfo()[self.tower.getLevel() + 1]["costs"])
    

    def updatePrice(self, resources):
        """ Changes costs displayed and colors """
        if not self.displayPrice: return False

        price = self.getUpgradeCost()
        for resource, amount in resources.items():
            text = super().getObj(resource + "Cost")
            text.changeText(str(price[resource]))

            if amount < price[resource]: 
                text.changeColor([ 255, 0, 0 ])
            else: 
                text.changeColor([ 0, 0, 0 ])
    

    def update(self, window, resources):
        """ Updates buttons and prices on upgrade screen"""
        super().update(window)
        if not super().isDisplaying(): return None
            
        self.updatePrice(resources)

        if self.displayPrice and resources >= self.getUpgradeCost():
            super().getObj("upgrade").setDisplaying(True)
            
            self.bought = False

            if super().getObj("upgrade").getPressed():
                self.tower.upgrade()
                self.selectTower(self.tower)
                self.bought = True

        else:
            super().getObj("upgrade").setDisplaying(False)
            self.bought = False
    
    
    def getBought(self): return self.bought
    def getTower(self): return self.tower