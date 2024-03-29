import pygame
import logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.tileset import Tileset
from src.utility.advDict import AdvDict
from  src.entities.tower import Tower
from src.waves import Waves

from src.ui.shop import Shop
from src.ui.upgrade import UpgradeMenu
from src.ui.error import Error
from src.ui.deathScreen import DeathScreen
from src.ui.pause import PauseMenu
from src.ui.warning import Warning

class Round:
    """ Handles the game content, such as the world, tileset, and towers
        for every game that the player plays. """
    
    towersJson = None
    shopData = None

    def __init__(self, map, consts, uiData, saveDatabase, prevHighscore, musicVolume, sfxVolume):
        """ Setup tileset object, etc. """
        self.log = logging.getLogger(__name__)

        self.map = map
        self.consts = consts

        self.tileset = Tileset(map, consts)
        self.tileset.playMusic(musicVolume)
        self.sfxVolume = sfxVolume

        self.waves = Waves(consts)
        
        try:
            self.towersJson = util.loadJson(consts["jsonPaths"]["towers"])
        except KeyError as exc:
            Error.createError("Unable to find the required paths to JSON files within the constants JSON.", self.log, exc)

        self.shop = Shop(consts, uiData, self.towersJson)
        self.upgradeMenu = UpgradeMenu(consts, uiData)
        
        # Make rectangle of size of the window screen
        windowSize = Vect(consts["window"]["size"]).getTuple()
        bgShade = pygame.Surface(windowSize)
        bgShade.fill((0, 0, 0)) # Fill with black
        bgShade.set_alpha(100) # Set semi-transparent
        # For background of the pause and death screens

        self.deathScreen = DeathScreen(consts, uiData, bgShade)
        self.pauseMenu = PauseMenu(consts, uiData, bgShade)
        self.warning = Warning(consts, uiData, bgShade)

        self.saveDatabase = saveDatabase
        self.prevHighscore = prevHighscore
        
        self.towers = []

        try:
            # Default resources
            self.resources = AdvDict(consts["startingResources"].copy())
        except KeyError as exc:
            Error.createError("Unable to find starting resources for the player in the constants JSON file.", self.log, exc)
    
    
    def update(self, window, consts):
        """ Updates everything for the frame """
        # Normal game, no pause or death screen up
        if not self.deathScreen.isDisplaying() and not self.pauseMenu.isDisplaying() and not self.warning.isDisplaying():
            # Updating each section of the game
            self.tileset.update(window, consts)
            self.waves.update(window, self.tileset, self.consts)
            self.resources += self.waves.getFrameDrops() # Adding any enemy drops
            self.capResources() # Cap resources at 999
            
            self.updateTowers(window, consts)

            self.shop.update(window, self.resources, self.upgradeMenu.isDisplaying(), 
                             self.isPlacingATower(), self.waves, self.tileset)

            self.upgradeMenu.update(window, self.resources)

            self.warning.detect(self.waves)

            # Checking buttons
            self.checkPurchases()
            self.checkDeath()
            self.checkSkipButton()
            self.checkPauseButton(window)

            # Player pressed "sell" button in upgrades menu
            if self.upgradeMenu.isSold():
                self.log.info("Selling tower")
                self.upgradeMenu.setSold(False)
                self.resources += self.upgradeMenu.getSellPrice() # Adding sell price
                self.towers.pop(self.upgradeMenu.getTowerIndex()) # Removing tower
        
        # Death screen
        elif self.deathScreen.isDisplaying():
            self.deathScreen.update(window)
        
        # Pause menu
        elif self.pauseMenu.isDisplaying():
            self.pauseMenu.update(window)
        
        elif self.warning.isDisplaying():
            self.warning.update(window)


    def updateTowers(self, window, consts):
        """ Updates towers and tower selecting """
        noTowers = True # Testing if the player has a tower selected

        # Iterate through towers and update them
        for index, tower in enumerate(self.towers):
            tower.update(window, self.tileset, self.waves, consts)

            if tower.justSelected(): 
                if not self.isPlacingATower(): # If not currently placing a tower
                    self.upgradeMenu.selectTower(tower, index) # Display upgrades
                    
                else:
                    # A tower is being placed, and the player just clicked on a different tower
                    tower.unselect()
            
            if tower.isSelected(): noTowers = False

        if self.upgradeMenu.isDisplaying() and noTowers:
            self.upgradeMenu.setDisplaying(False)


    def checkPurchases(self):
        """ Checks and handles the event of the player pressing the "buy" button """
        if self.shop.getBought():
            # Charging the player for the resources
            self.resources -= AdvDict(self.shop.getTowerPrice())
            # Adding the tower to the tower list
            self.towers.append(Tower(self.shop.getSelectedTowerName(), self.towersJson, self.sfxVolume))
        
        elif self.upgradeMenu.getBought():
            self.resources -= AdvDict(self.upgradeMenu.getTower().getCurrentCosts())
    

    def checkDeath(self):
        """ Checks player health """
        if self.waves.playerIsDead():
            self.deathScreen.showDeath(self.prevHighscore, self.waves.getWaveNum() + 1)
    

    def checkSkipButton(self):
        """ Checks if the player pressed the skip forward button in the shop """
        if self.shop.skipButtonPressed():
            self.waves.skipWaveDelay()
    

    def checkPauseButton(self, window):
        """ Checks if the player pressed the pause button or pressed escape """
        if self.shop.pauseButtonPressed() or window.getEscapeKey():
            self.pauseMenu.setDisplaying(True)
    
    
    def capResources(self):
        """ Caps resources at 999, so they don't overlap the UI """
        for resource in self.resources.keys():
            if self.resources[resource] > 999:
                self.resources[resource] = 999
    
    
    def render(self, window, consts):
        """ Render tileset, enemies, and towers and UI """
        self.tileset.renderTiles(window) # Render tiles
        self.waves.render(window) # Render enemies
        self.tileset.renderDeco(window)
        self.renderTowers(window, consts) # Render towers

        # Render shop and upgrades menu
        self.shop.render(window) 
        self.upgradeMenu.render(window)

        # Render deathscreen or pause if they're displaying or the warning message
        self.deathScreen.render(window) 
        self.pauseMenu.render(window)
        self.warning.render(window)

    
    
    def renderTowers(self, window, consts):
        """ Renders towers in order from the top to the bottom of the map
            in order to prevent tower overlap in the wrong direction """

        height = self.tileset.getTilesSize().y

        for row in range(height): # Iterate through rows top to bottom
            for tower in self.towers:
                if tower.getTileOn() == None: continue

                elif tower.getTileOn().getCoords().y == row: # Render this row of towers
                    tower.render(window)
        
        # Render tower range circle if it's selected
        for tower in self.towers:
            tower.renderRange(window, consts)
    
    
    def isPlacingATower(self):
        """ Returns true if there is a tower being placed currently """
        for tower in self.towers:
            if tower.isPlacing():
                return True
        
        return False
    

    def unselectTowers(self):
        """ Unhighlights every tower, turning off showRange """
        for tower in self.towers:
            tower.unselect()
    

    def isGameOver(self):
        return self.deathScreen.pressedContinue() or self.pauseMenu.getQuitPressed()
    

    def stopMusic(self):
        self.tileset.stopMusic()

    
    def save(self):
        """ Changes wave highscore in the save database if it's a new highscore """
        waveNum = self.waves.getWaveNum() + 1

        if waveNum > self.prevHighscore:
            self.log.info("Saving highscore")
            
            if self.saveDatabase.findValue("waveHighscores", "highscore", "map", self.map) != None:
                self.saveDatabase.modify("waveHighscores", "map", self.map, "highscore", waveNum)
            else:
                self.saveDatabase.insert("waveHighscores", self.map, waveNum)