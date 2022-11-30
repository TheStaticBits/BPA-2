import pygame
import logging

from src.ui.ui import UI

class Error(UI):
    """ Displays error message and gives the user options for how to handle the error """
    errored = False

    def __init__(self, consts, uiData):
        super().__init__(self, __name__)

        super().load(consts, "error", uiData)


    def update(self, window):
        """ Handles error button presses """
        super().update(window)
    

    @staticmethod
    def createError(self, errorMsg, recoverable=False):
        """ Call this static method whenever there is an error to update and display the error report box """
        errored = True

        textTitle = super().getObj("title")

        if recoverable:
            textTitle.changeText("An exception occured. This is a recoverable state.")
        else:
            textTitle.changeText("An error occured. This is nonrecoverable.")

        super().setDisplaying(True)
    

    def hasError(self): return self.errored