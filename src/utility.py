import pygame
import logging
import json
import os

import src.enemy as enemy
from src.vector import Vect

imgScale = 1

def loadFile(path):
    """ Loads text file """
    with open(path) as f:
        return f.read()

def loadJson(path):
    """ Loads JSON file """
    with open(path) as f:
        return json.load(f)

def loadTex(path):
    """ Loads texture that is not trasparent. 
        The pygame convert() function is speedier than pygame's convert_alpha(), 
        although any transparency will be removed. """ 
    return scale(pygame.image.load(path).convert())

def loadTexTransparent(path):
    """ Loads transparent texture.
        Slower than normal loadTex due to including alpha values. """
    return scale(pygame.image.load(path).convert_alpha())

def scale(img: pygame.Surface):
    """ Scales up to the default image scale and returns it """
    if imgScale == 1: return img

    size = Vect(img.get_size())
    return pygame.transform.scale(img, (size * imgScale).getTuple())


def rectCollision(pos1: Vect, size1: Vect, 
                  pos2: Vect, size2: Vect):
    """ Checks rectangle collision with given Vect objects """
    return ( pos1.x < pos2.x + size2.x and 
             pos2.x < pos1.x + size1.x and 
             pos1.y < pos2.y + size2.y and
             pos2.y < pos1.y + size1.y )

def pointRectCollision(point: Vect, pos: Vect, size: Vect):
    return pos <= point < (pos + size)

def pixelPerfectCollision(entity1=None,         entity2=None,
                          img1=None, pos1=None, img2=None, pos2=None):
    """ Uses Pygame mask objects to detect pixel perfect collisions """

    if entity1 != None and entity2 != None:
        ent1Mask = pygame.mask.from_surface(entity1.getAnim().getImgFrame())
        ent2Mask = pygame.mask.from_surface(entity2.getAnim().getImgFrame())

        offset = entity2.getPos() - entity1.getPos()
    
    else:
        ent1Mask = pygame.mask.from_surface(img1)
        ent2Mask = pygame.mask.from_surface(img2)

        offset = pos2 - pos1

    return ent1Mask.overlap(ent2Mask, offset.getTuple())


def setupLogger(constants):
    """ Setup the Python logger for use """
    logger = logging.getLogger("")

    # If the folder that the event.log is in does not exist, create it
    paths = constants["log"]["output"].split("/")
    # Creates string of the directory to the file, not including the 
    # file (last element of the path)
    path = "/".join([i for n, i in enumerate(paths) if n != len(paths) - 1])
    if not os.path.exists(path):
        os.makedirs(path)
    
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