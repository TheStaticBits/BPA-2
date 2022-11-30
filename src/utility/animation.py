import pygame
import logging

import src.utility.utility as util
from src.utility.timer import Timer
from src.utility.vector import Vect

class Animation:
    """ Handles animations (only horizontal spritesheets) """
    def __init__(self, img, frameCount, delay):
        """ Loads animation """
        self.log = logging.getLogger(__name__)

        self.imgs = []

        if isinstance(img, str): # If img parameter is the path 
            self.log.info(f"Loading animation at \"{img}\"")
            img = util.loadTexTransparent(img) # Entire animation
        
        size = Vect(img.get_size())
        frameSize = Vect(size.x // frameCount, size.y)

        self.timer = Timer(delay)
        self.totalFrames = frameCount
        self.currentFrame = 0
        self.hasFinished = False
        self.flippedFrame = False

        # Creating each frame image and adding it to the list of the animation frame images
        for i in range(frameCount):
            frame = pygame.Surface(frameSize.getTuple(), 
                                   flags=pygame.SRCALPHA)
            frame.blit(img, (-i * frameSize.x, 0), 
                       special_flags=pygame.BLEND_RGBA_MAX)
            self.imgs.append(frame)

    
    def update(self, window):
        """ Moves to the next frame if the delay is up """
        self.hasFinished = False
        self.flippedFrame = False

        self.timer.update(window)

        if self.timer.activated():
            self.currentFrame += 1
            self.flippedFrame = True

            if self.currentFrame >= self.totalFrames:
                self.currentFrame = 0
                self.hasFinished = True
    

    def render(self, window, pos):
        """ Renders the current frame at pos """
        window.render(self.imgs[self.currentFrame], pos)


    # Getters
    def getImgFrame(self):
        """ Returns the texture of the current frame of the animation """ 
        return self.imgs[self.currentFrame]

    def getSize(self):   return Vect(self.imgs[0].get_size())
    def getWidth(self):  return self.getSize().x
    def getHeight(self): return self.getSize().y
    
    def getFrameNum(self): return self.currentFrame
    def getFrame(self, frame): return self.imgs[frame]

    def finished(self): return self.hasFinished
    def changedFrame(self): return self.flippedFrame