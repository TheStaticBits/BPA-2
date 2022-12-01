import pygame
import logging
import traceback

from src.ui.ui import UI

class Error(UI): # Inherits from the UI class in src/ui/ui.py
    """ Displays exception/error message and gives the user options for how to handle it """
    errored = False
    crashed = False

    def __init__(self, consts, uiData):
        super().__init__(self, __name__)

        super().load(consts, "error", uiData) # Loading UI objects from the UI data in the JSON file


    def update(self, window):
        """ Handles error button presses """
        super().update(window)

        if super().getObj("continue").getPressed():
            self.errored = False
    

    @staticmethod
    def createError(self, logMessage, logger, exceptionObj, recoverable=False):
        """ Call this static method whenever there is an error to update and display the error report box """
        self.errored = True

        # Logging the given message and the exception object
        logger.error(f"Exception caught while {logMessage}.\n(see error textbox or text file for more information)\n{str(exceptionObj)}")

        # Includes error traceback, with file and line number
        detailedErrorMsg = traceback.format_exc()

        # Updating error message box with the error
        super().getObj("errorMsg").changeText(detailedErrorMsg)

        textTitle = super().getObj("title")

        if recoverable:
            textTitle.changeText("An exception occured. This is a recoverable state.")
            # Gets the Button object, getting the Text object of the button object, and changing the text to "Continue"
            super().getObj("continue").getText().changeText("Continue")
        else:
            textTitle.changeText("An error occured. This is nonrecoverable.")
            # Changing the text of the button to "Close Game"
            super().getObj("continue").getText().changeText("Close Game")
            self.crashed = True

        super().setDisplaying(True)
    

    def showingError(self): return self.errored
    def hasCrashed(self): return self.crashed