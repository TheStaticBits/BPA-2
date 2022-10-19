import pygame
import logging

import src.utility as util

class Animation:
    """ Handles animations (only horizontal spritesheets) """
    def __init__(self, path, frameCount, delay):
        """ Loads animation """
        self.log = logging.getLogger(__name__)

        self.log.info(f"Loading animation at \"{path}\"")

        self.imgs = []
        img = util.loadTexTransparent(path) # Entire animation
        size = self.getSize()
        frameSize = Vect(size.x // frameCount, size.y)

        self.delay = delay
        self.totalFrames = frameCount

        # Creating each frame 
        for i in range(frameCount):
            frame = pygame.Surface(frameSize.getTuple())
            frame.blit(img, (-i * frameSize.x, 0))
            self.imgs.append(frame)

        self.timer = 0
        self.currentFrame = 0
    

    def __init__(self, animData):
        """ Loads data from a dictionary of animation data """
        
        self.__init__( animData["path"], 
                       animData["frames"], 
                       animData["delay"] ) 


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