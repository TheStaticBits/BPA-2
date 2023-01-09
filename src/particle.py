import pygame
import logging
import random
import math

from src.utility.vector import Vect
from src.ui.error import Error
from src.utility.timer import Timer

class Particle:
    """ Handles a single particle """
    def __init__(self, constsJson, pos, image, moveAngle):
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

        imgOffset = Vect( random.randint(0, imageSize.x - size.x),
                          random.randint(0, imageSize.y - size.y) )
        
        # Multiplying by -1 to get the offset of the original image
        imgOffset *= -1

        self.img = pygame.Surface(size.getTuple(), flags=pygame.SRCALPHA)

        # Offsets image to slice out a random chunk of the image for the particle
        self.img.blit(image, imgOffset.getTuple())
    

    def update(self, window):
        """ Updates particle, moving it, updating its timer, etc. """
        self.timer.update(window)

        percentDone = self.timer.getPercentDone()
        # When the timer is 60 percent done, start adding transparency to the 
        # particle based on how much percent is left.
        if percentDone > 0.6:
            percent = (percentDone - 0.6 ) / 0.4 # Percent of the last 40 percent of time left
            self.img.set_alpha( (1 - percent) * 255 )

        self.pos.x += math.cos(self.moveAngle) * self.speed * window.getDeltaTime()
        self.pos.y += math.sin(self.moveAngle) * self.speed * window.getDeltaTime()

    
    def render(self, window):
        window.render(self.img, self.pos)


    def isDone(self):
        return self.timer.activated()