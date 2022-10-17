import pygame
import logging

import src.utility as util

class Animation:
    """ Handles animations (only horizontal spritesheets) """
    def __init__(self, path, frameCount, delay):
        """ Loads animation """
        self.log = logging.getLogger(__name__)

        self.imgs = []
        img = util.loadTexTransparent(path) # Entire animation
        size = img.get_size()
        frameSize = (size[0] // frameCount, size[1])

        self.delay = delay
        self.totalFrames = frameCount

        # Creating each frame 
        for i in range(frames):
            frame = pygame.Surface(frameSize)
            frame.blit(img, (-i * frameSize[0], 0))
            self.imgs.append(frame)

        self.timer = 0
        self.currentFrame = 0


    def update(self, window):
        """ Moves to the next frame if the delay is up """

        self.timer += window.getDeltaTime()

        if self.timer > self.delay:
            self.timer = 0
            self.currentFrame += 1

            if self.currentFrame > self.totalFrames:
                self.currentFrame = 0
    

    def render(self, window, pos):
        """ Renders the current frame at pos """
        window.render(self.imgs[self.currentFrame], pos)
    

    # Getters
    def getSize(self):   return self.frames[0].get_size()
    def getWidth(self):  return self.getSize()[0]
    def getHeight(self): return self.getSize()[1]