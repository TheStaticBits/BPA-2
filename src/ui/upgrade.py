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
    

    def format(self, stats):
        """ Takes in tower stats dictionary and formats it for display """
        return { "Range": int(stats["range"] / 10),
                 "Damage": stats["damage"],
                 "Speed": int(10 / stats["attackCooldown"]) }
    

    def selectTower(self, tower):
        """ Chooses a tower to show the upgrade menu for """

        super().setDisplaying(True)
        self.tower = tower
        
        # Change tower name displayed, upgrade level, image, price of upgrade, and upgrade stats here
        super().getObj("towerName").changeText(tower.getType())
        super().getObj("upgradeLevel").changeText(f"Lvl: {tower.getLevel() + 1}")

        towerStats = self.format(tower.getCurrentStats())
        towerStatsStr = "\n".join(f"{key}: {value}" for key, value in towerStats.items())

        super().getObj("towerStats").changeText(towerStatsStr)

        # If the tower has another level to upgrade to
        if len(tower.getUpgradeInfo()) - 1 > tower.getLevel():
            super().getObj("upgradeStats").setDisplaying(True)
            super().getObj("upgrade").setDisplaying(True)

            newTowerStats = self.format(tower.getUpgradeInfo()[tower.getLevel() + 1]["stats"])

            # Find difference between current stats and stats of a level above
            diff = {}
            for key in towerStats.keys():
                diff[key] = newTowerStats[key] - towerStats[key]

            statsStr = "\n".join(f"+{value} {key}" for key, value in diff.items())
            super().getObj("upgradeStats").changeText(statsStr)

        else:
            super().getObj("upgradeStats").setDisplaying(False)
            super().getObj("upgrade").setDisplaying(False)
        
        super().getObj("tower").setImg(tower.getImg())
    

    def update(self, window):
        super().update(window)

        self.bought = False
        if super().getObj("upgrade").getPressed():
            self.tower.upgrade()
            self.selectTower(self.tower)
            self.bought = True