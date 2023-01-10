import pygame
import logging

from src.ui.ui import UI
from src.ui.error import Error
from src.utility.database import DatabaseHandler
from src.tileset import Tileset
from src.waves import Waves

class MainMenu(UI):
    def __init__(self, consts, uiData, saveDatabase):
        super().__init__(True, __name__)
        
        super().load(consts, "mainMenu", uiData) # Loading UI objects for specifically the upgrades menu
        
        try:
            self.mapsDict = consts["maps"]
            self.mapsOrder = list(self.mapsDict.keys()) # Gets map folder names in a list
            self.loadedMaps = {}
        except KeyError as exc:
            Error.createError("Failed to retrieve maps from constants JSON.", self.log, exc)
        

        try:
            bgMap = consts["backgroundMaps"]["mainMenu"]
        except KeyError as exc:
            Error.createError("Unable to find background map name for the main menu in constants.json", self.log, exc)
        

        self.music = None
        try:
            self.music = pygame.mixer.Sound(consts["music"]["mainMenu"])
        except KeyError as exc:
            Error.createError("Unable to find main menu music in constants.json. Not playing music.", self.log, exc, recoverable=True)

        
        self.bgTilset = Tileset(bgMap, consts)
        self.bgEnemies = Waves(consts)
        
        self.mapShown = 0 # index of map in self.mapsOrder
        self.consts = consts
        self.saveDatabase = saveDatabase

        # Creating table if there isn't one already for storing settings such as volume
        self.saveDatabase.createTable("settings", "name TEXT, value INTEGER")
        self.findVolume()
        
        self.playMusic()

        self.updateMapShown()
    

    def playMusic(self):
        """ Play music on loop """
        self.music.set_volume(self.getMusicVolume())
        self.music.play(-1)
    
    def stopMusic(self):
        self.music.stop()
    

    def findVolume(self):
        """ Finding sfx and music volumes in the save database """
        self.sfxVolume = self.saveDatabase.findValue("settings", "value", "name", "sfxVolume")
        self.musicVolume = self.saveDatabase.findValue("settings", "value", "name", "musicVolume")

        # If the user has or has not saved volume settings by closing the game yet
        self.volumeIsSaved = not (self.sfxVolume is None)

        # Set to default of 50
        if not self.volumeIsSaved: 
            self.sfxVolume = 50
            self.musicVolume = 50
        else: # fetchone returns a tuple, choose first value
            self.sfxVolume = self.sfxVolume[0]
            self.musicVolume = self.musicVolume[0]
    

    def updateMapShown(self):
        """ Updates UI for a new map shown on screen to the user """
        if self.getSelectedMap() not in self.loadedMaps:
            mapTiles = Tileset(self.getSelectedMap(), self.consts)
            mapImage = pygame.Surface(mapTiles.getBoardSize().getTuple())

            # Draw tiles to mapImage
            mapTiles.renderToSurf(mapImage)

            mapImage = pygame.transform.scale(mapImage, ( 250, 250 ))

            self.loadedMaps[self.getSelectedMap()] = mapImage

        super().getObj("map").setImg(self.loadedMaps[self.getSelectedMap()])
        super().getObj("mapName").setText(self.mapsDict[self.getSelectedMap()])


        self.highscore = self.saveDatabase.findValue("waveHighscores", "highscore", "map", self.getSelectedMap())
        if self.highscore == None: 
            self.highscore = 0 # If the map hasn't been played yet
        else:
            self.highscore = self.highscore[0]

        super().getObj("highscore").setText(f"Wave Highscore: {self.highscore}")
    

    def updateBG(self, window, consts):
        """ Updates background tileset and enemies of main menu (and for tutorial background) """
        self.bgTilset.update(window, consts, animateTile=False)
        self.bgEnemies.update(window, self.bgTilset, consts)


    def update(self, window, consts):
        """ Updates button functionality on main menu """

        self.updateBG(window, consts)

        super().update(window)
        
        self.checkMapButtons()
        self.checkVolumeButtons()

        if self.getVolumeChanged():
            self.music.set_volume(self.getMusicVolume())
    

    def checkMapButtons(self):
        """ Checks if left or right buttons on the menu have been pressed """
        if super().getObj("left").getPressed():
            self.mapShown -= 1
            if self.mapShown < 0:
                self.mapShown = len(self.mapsOrder) - 1
            self.updateMapShown()
        
        elif super().getObj("right").getPressed():
            self.mapShown += 1
            if self.mapShown >= len(self.mapsOrder):
                self.mapShown = 0
            self.updateMapShown()
    
    
    def checkVolumeButtons(self):
        """ Checks the volume buttons of being pressed """
        self.volumeChanged = False

        # Music volume up and down buttons
        if super().getObj("musicVolumeUp").getPressed():
            self.musicVolume += 5
            if self.musicVolume > 100: self.musicVolume = 100
            self.volumeChanged = True
        elif super().getObj("musicVolumeDown").getPressed():
            self.musicVolume -= 5
            if self.musicVolume < 0: self.musicVolume = 0
            self.volumeChanged = True
        
        # SFX volume up and down buttons
        if super().getObj("sfxVolumeUp").getPressed():
            self.sfxVolume += 5
            if self.sfxVolume > 100: self.sfxVolume = 100
            self.volumeChanged = True
        elif super().getObj("sfxVolumeDown").getPressed():
            self.sfxVolume -= 5
            if self.sfxVolume < 0: self.sfxVolume = 0
            self.volumeChanged = True

        super().getObj("musicVolume").setText(f"{self.musicVolume}%")
        super().getObj("sfxVolume").setText(f"{self.sfxVolume}%")
    

    def renderBG(self, window):
        """ Renders background tileset and enemies """
        self.bgTilset.renderTiles(window)
        self.bgTilset.renderDeco(window)
        self.bgEnemies.render(window)
    

    def render(self, window):
        """ Renders background enemies and tileset and the UI elements """
        self.renderBG(window)
        super().render(window)

    
    def pressedPlay(self):
        """ Returns true if the play button was pressed on the frame """
        return super().getObj("play").getPressed()
    
    def getSelectedMap(self):
        """ Returns the name of the map chosen """
        return self.mapsOrder[self.mapShown]
    

    def saveVolume(self):
        """ Saves volume settings to the database """
        if self.volumeIsSaved: # In the database already, so just modify it
            self.saveDatabase.modify("settings", "name", "sfxVolume", "value", self.sfxVolume)
            self.saveDatabase.modify("settings", "name", "musicVolume", "value", self.musicVolume)
        else: # Not yet in the database, insert it
            self.saveDatabase.insert("settings", "sfxVolume", self.sfxVolume)
            self.saveDatabase.insert("settings", "musicVolume", self.musicVolume)
    

    def getHighscore(self): return self.highscore
    def getTutorialButton(self): return super().getObj("tutorial").getPressed()

    def getVolumeChanged(self): return self.volumeChanged
    def getMusicVolume(self): return self.musicVolume * 0.01
    def getSFXVolume(self): return self.sfxVolume * 0.01