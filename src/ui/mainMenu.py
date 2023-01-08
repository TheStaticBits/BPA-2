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
        
        self.bgTilset = Tileset(bgMap, consts)
        self.bgEnemies = Waves(consts)
        
        self.mapShown = 0 # index of map in self.mapsOrder
        self.consts = consts
        self.saveDatabase = saveDatabase

        self.updateMapShown()
    

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


    def update(self, window, consts):
        """ Updates button functionality on main menu """

        self.bgTilset.update(window, consts, animateTile=False)
        self.bgEnemies.update(window, self.bgTilset, consts)

        super().update(window)

        # Left and right buttons on the menu
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
    

    def render(self, window):
        """ Renders background enemies and tileset and the UI elements """
        self.bgTilset.renderTiles(window)
        self.bgTilset.renderDeco(window)
        self.bgEnemies.render(window)

        super().render(window)

    
    def pressedPlay(self):
        """ Returns true if the play button was pressed on the frame """
        return super().getObj("play").getPressed()
    
    def getSelectedMap(self):
        """ Returns the name of the map chosen """
        return self.mapsOrder[self.mapShown]
    

    def getHighscore(self): return self.highscore