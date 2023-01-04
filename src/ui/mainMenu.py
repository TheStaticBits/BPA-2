import pygame
import logging

from src.ui.ui import UI
from src.ui.error import Error
from src.utility.database import DatabaseHandler
from src.tileset import Tileset

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

        super().getObj("highscore").setText(f"Wave Highscore: {self.highscore}")


    def update(self, window):
        """ Updates button functionality on main menu """
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

    
    def pressedPlay(self):
        """ Returns true if the play button was pressed on the frame """
        return super().getObj("play").getPressed()
    
    def getSelectedMap(self):
        """ Returns the name of the map chosen """
        return self.mapsOrder[self.mapShown]
    

    def getHighscore(self): return self.highscore