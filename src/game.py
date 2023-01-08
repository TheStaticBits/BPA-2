import pygame
import logging

import src.utility.utility as util
from src.window import Window
from src.round import Round
from src.ui.error import Error
from src.ui.mainMenu import MainMenu
from src.utility.database import DatabaseHandler

class Game:
    """ Handles scenes and the functionality of the entire game """
    def __init__(self):
        """ Loads game data and needed scene objects """

        self.constants = util.loadJson("data/constants.json")
        self.uiData = util.loadJson(self.constants["jsonPaths"]["ui"])

        util.imgScale = self.constants["game"]["imgScale"]

        # Setup logging
        util.setupLogger(self.constants)
        self.log = logging.getLogger(__name__)
        
        self.scene = "mainMenu"

        try:
            # Init objects
            self.log.info("Loading game...")
            
            self.window = Window(self.constants)

            # Save file
            self.save = DatabaseHandler(self.constants["log"]["saveFile"])
            self.save.createTable("waveHighscores", "map TEXT, highscore INTEGER")
            # Creates database table if not already created
            
            # Error menu handler
            self.errorUI = Error(self.constants, self.uiData)
            self.mainMenu = MainMenu(self.constants, self.uiData, self.save)

        except Exception as exc:
            Error.createError("Error occured while loading game", self.log, exc)
    

    def startLoop(self):
        """ Game loop, with window updating and rendering, inputs, and game content """
        
        while not self.window.isClosed() and not self.errorUI.hasCrashed():
            self.window.handleInputs()
            
            self.errorUI.update(self.window)
            self.errorUI.render(self.window)
            
            if not self.errorUI.isDisplaying():
                if self.errorUI.hasCrashed():
                    break # User pressed "Close Game" on error menu

                # Run a frame
                try:
                    self.runFrame()

                except Exception as exc:
                    Error.createError("An unhandled error occured while the game was running.", self.log, exc)

            
            self.window.update(self.constants)

        self.saveAndClose()
    

    def runFrame(self):
        if self.scene == "mainMenu":
            self.mainMenu.update(self.window)
            self.mainMenu.render(self.window)

            if self.mainMenu.pressedPlay():
                self.round = Round(self.mainMenu.getSelectedMap(), self.constants, 
                                   self.uiData, self.save, self.mainMenu.getHighscore())

                self.scene = "round"

        elif self.scene == "round":
            self.round.update(self.window, self.constants)
            self.round.render(self.window, self.constants)

            if self.round.isGameOver():
                self.scene = "mainMenu"
                self.round.save()
                self.mainMenu.updateMapShown()
                self.round.stopMusic()
                del self.round
    

    def saveAndClose(self):
        """ Saves highscore and closes database """
        if self.scene == "round": # If the player closed in the middle of a round
            self.round.save()

        self.save.close()