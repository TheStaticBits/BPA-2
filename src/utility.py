import pygame
import logging
import json

def loadJson(filePath):
    """ Loads JSON file """
    with open(filePath) as f:
        return json.load(f)

def loadTex(path):
    """ Loads texture that is not trasparent. 
        The pygame convert() function is speedier than pygame's convert_alpha(), 
        although any transparency will be removed. """ 
    return pygame.image.load(path).convert()

def loadTexTransparent(path):
    """ Loads transparent texture.
        Slower than normal loadTex due to including alpha values. """
    return pygame.image.load(path).convert_alpha()


def setupLogger(constants):
    """ Setup the Python logger for use """
    logger = logging.getLogger("")
    
    # Set level based on what is set in constants JSON file
    if   (constants["log"]["level"] == "DEBUG"):   logger.setLevel(logging.DEBUG)
    elif (constants["log"]["level"] == "WARNING"): logger.setLevel(logging.WARNING)
    else:                                          logger.setLevel(logging.INFO)

    fileFormatter =    logging.Formatter("[%(asctime)s] - [%(levelname)s] %(name)s: %(message)s")
    consoleFormatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    
    fileHandler =    logging.FileHandler(constants["log"]["output"])
    consoleHandler = logging.StreamHandler()

    fileHandler.setFormatter(fileFormatter)
    consoleHandler.setFormatter(consoleFormatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)