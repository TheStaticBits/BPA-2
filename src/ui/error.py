import pygame
import logging
import traceback
import os

# for email crash reporting
import smtplib, ssl
import base64
from email.message import EmailMessage
from datetime import datetime

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
        
        # Loading data from constants.json
        try:
            self.errorFilePath = consts["log"]["errors"]
        except KeyError as exc:
            self.createError("Error loading error file path", super().getLogger(), exc)
        
        try:
            self.email = consts["emailReporting"]["email"]
            self.pwd = consts["emailReporting"]["encodedPassword"]
            self.numberOfLogs = consts["emailReporting"]["numberOfLogs"]

        except KeyError as exc:
            self.createError("Error loading email reporter info from constants JSON.", super().getLogger(), exc)
        
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
                self.emailCrash()
            
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

        # Logging the given message using the given logger and the given exception object
        logger.error(f"Exception: {logMessage}\n(see error textbox or text file for more information)\n{str(exceptionObj)}")

        if not cls.errored: # If there's not already an error on screen
            cls.errored = True
            cls.recoverable = recoverable

            # Includes error traceback, with file and line number
            cls.errorMsg = traceback.format_exc()
            print("\n" + cls.errorMsg + "\n")
    

    def testForError(self):
        """ Updates UI elements if it detects an error has occured """
        
        if self.errored: # An error has occured! (something has called createError())
            self.errored = False

            super().setDisplaying(True) # Set error UI to be displaying
            
            # Updating error message box with the error
            super().getObj("errorMsg").setText(self.errorMsg)
            
            # Appending the error to the error text file
            if isinstance(self.errorFilePath, str):
                with open(self.errorFilePath, "a") as file:
                    file.write(self.errorMsg)

            textTitle = super().getObj("title")

            # Recoverable means whether or not the program can continue running after the error has occured
            if self.recoverable:
                textTitle.setText("A recoverable error occured:")
                # Gets the Button object, getting the Text object of the button object, and changing the text to "Continue"
                super().getObj("continue").getTextObj().setText("Continue")
            else:
                textTitle.setText("A nonrecoverable error occured:")
                # Changing the text of the button to "Close Game"
                super().getObj("continue").getTextObj().setText("Close Game")
    

    def emailCrash(self):
        """ Emails the error and some log lines above the crash to our email """
        
        self.log.info("Emailing error")

        # Decode email password from base64
        pwd = base64.b64decode(self.pwd).decode("utf-8")

        # Loading logs to include some in the email
        with open(self.logsFilePath, "r") as file:
            logs = file.read()

        # Removes everything in the logs list but the last number of lines
        logs = logs.split("\n")
        logs = logs[-self.numberOfLogs:]

        emailBody = Error.errorMsg + "\n"
        emailBody += "\n".join(logs) # Turns list into string separated by newlines

        self.log.info("Compiling email message")

        # Sending crash error and logs from the email to the same email
        # for developers to look at
        message = EmailMessage()
        message["Subject"] = str(datetime.now()) # current time as the email subject
        message["From"] = self.email
        message["To"] = self.email
        message.set_content(emailBody)

        self.log.info("Sending email")

        # Logging in and sending through SMPT Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(self.email, pwd)
            s.send_message(message)
    

    def hasCrashed(self): 
        return self.crashed