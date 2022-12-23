import pygame
import logging
import random
import math

from src.utility.vector import Vect
from src.ui.error import Error
from src.utility.timer import Timer

class Particle:
    """ Handles a single particle"""
    def __init__(self, constsJson, pos, size, image, moveAngle):
        """ Chooses a random position in the image to be in the particle image """
        self.log = logging.getLogger(__name__)
        
        self.pos = pos
        self.moveAngle = math.radians(moveAngle)

        try:
            self.speed = constsJson["game"]["particles"]["speed"]
            self.timer = Timer(constsJson["game"]["particles"]["lastDuration"])
            size = Vect(constsJson["game"]["particles"]["size"])
        
        except Exception as exc:
            Error.createError("Error loading particles JSON data from constants JSON file", self.log, exc)

        # Finding random position in the image for size
        imageSize = Vect(image.get_size())

        imgOffset = -Vect( random.randint(0, imageSize.x - size.x),
                           random.randint(0, imageSize.y - size.y) )

        self.img = pygame.Surface(size.getTuple(), flags=pygame.SRCALPHA)

        # Offsets image to slice out a random chunk of the image for the particle
        self.img.blit(image, imgOffset.getTuple())
    

    def update(self, window):
        self.timer.update(window)

        self.pos.x += math.cos(self.moveAngle) * self.speed
        self.pos.y += math.sin(self.moveAngle) * self.speed

    
    def render(self, window):
        window.render(self.img, self.pos)


    def isDone(self):
        return self.timer.activated()