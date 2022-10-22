import pygame
import logging

import src.utility as util
from src.vector import Vect

class Animation:
    """ Handles animations (only horizontal spritesheets) """
    def __init__(self, img, frameCount, delay):
        """ Loads animation """
        self.log = logging.getLogger(__name__)

        self.imgs = []

        if isinstance(img, str): # If img parameter is the path 
            self.log.info(f"Loading animation at \"{img}\"")
            img = util.loadTexTransparent(img) # Entire animation
        
        size = Vect(img.get_width() // frameCount, img.get_height())
        frameSize = Vect(size.x // frameCount, size.y)

        self.delay = delay
        self.totalFrames = frameCount

        # Creating each frame 
        for i in range(frameCount):
            frame = pygame.Surface(frameSize.getTuple(), 
                                   flags=pygame.SRCALPHA)
            frame.blit(img, (-i * frameSize.x, 0), 
                       special_flags = pygame.BLEND_RGBA_MAX)
            self.imgs.append(frame)

        self.timer = 0
        self.currentFrame = 0
    
    def update(self, window):
        """ Moves to the next frame if the delay is up """

        self.timer += window.getDeltaTime()

        if self.timer > self.delay:
            self.timer = 0
            self.currentFrame += 1

            if self.currentFrame >= self.totalFrames:
                self.currentFrame = 0
    

    def render(self, window, pos):
        """ Renders the current frame at pos """
        window.render(self.imgs[self.currentFrame], pos)
    

    # Getters
    def getSize(self):   return Vect(self.imgs[0].get_size())
    def getWidth(self):  return self.getSize().x
    def getHeight(self): return self.getSize().y