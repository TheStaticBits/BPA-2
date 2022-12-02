import pygame
import logging
import traceback
import os

import src.ui.ui as ui

class Error(ui.UI): # Inherits from the UI class in src/ui/ui.py
    """ Displays exception/error message and gives the user options for how to handle it """

    # Static variables for the static "createError" message to interact with,
    # allowing any methods that import this file to access and create an error
    errored = False
    errorMsg = None
    crashed = False
    recoverable = False

    def __init__(self, consts, uiData):
        super().__init__(False, __name__)

        super().load(consts, "error", uiData) # Loading UI objects from the UI data in the JSON file
        
        try:
            self.errorFilePath = consts["log"]["errors"]
        except KeyError as exc:
            self.createError("Error loading error file path", super().getLogger(), exc)
        
        self.logsFilePath = consts["log"]["output"]


    def update(self, window):
        """ Handles error button presses """
        super().update(window)

        if super().isDisplaying():
            # Button presses
            if super().getObj("continue").getPressed():
                self.errored = False
                super().setDisplaying(False)

                if not self.recoverable:
                    self.crashed = True
            
            if super().getObj("email").getPressed():
                self.log.info("Emailed crash information")
            
            if super().getObj("viewError").getPressed():
                # Opens the errors text file using the default text editor
                os.system("notepad " + self.errorFilePath) # Only works on Windows
            
            if super().getObj("viewLogs").getPressed():
                # Opens logs file using the default text editor
                os.system("notepad " + self.logsFilePath) # Only works on Windows

        else:
            self.testForError()
    

    @classmethod
    def createError(cls, logMessage, logger, exceptionObj, recoverable=False):
        """ Call this static method whenever there is an error to update and display the error report box """

        cls.errored = True
        cls.recoverable = recoverable

        # Logging the given message using the given logger and the given exception object
        logger.error(f"Exception: {logMessage}\n(see error textbox or text file for more information)\n{str(exceptionObj)}")

        # Includes error traceback, with file and line number
        cls.errorMsg = traceback.format_exc()
    

    def testForError(self):
        """ Updates UI elements if it detects an error has occured """
        
        if self.errored: # An error has occured! (something has called createError())
            self.errored = False

            super().setDisplaying(True) # Set error UI to be displaying
            
            # Updating error message box with the error
            super().getObj("errorMsg").changeText(self.errorMsg)
            
            # Appending the error to the error text file
            if isinstance(self.errorFilePath, str):
                with open(self.errorFilePath, "a") as file:
                    file.write(self.errorMsg)

            textTitle = super().getObj("title")

            # Recoverable means whether or not the program can continue running after the error has occured
            if self.recoverable:
                textTitle.changeText("A recoverable error occured:")
                # Gets the Button object, getting the Text object of the button object, and changing the text to "Continue"
                super().getObj("continue").getTextObj().changeText("Continue")
            else:
                textTitle.changeText("A nonrecoverable error occured:")
                # Changing the text of the button to "Close Game"
                super().getObj("continue").getTextObj().changeText("Close Game")
    

    def hasCrashed(self): 
        return self.crashed