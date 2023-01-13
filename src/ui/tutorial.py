import pygame
import logging

from src.ui.ui import UI
from src.ui.error import Error

class Tutorial(UI):
    """ Handles tutorial ui """

    def __init__(self, consts, uiData):
        super().__init__(True, __name__)
        
        super().load(consts, "tutorial", uiData)

        self.music = None
        try:
            self.music = pygame.mixer.Sound(consts["music"]["tutorial"])
        except KeyError as exc:
            Error.createError("Unable to find tutorial music. Not playing any music.", self.log, exc, True)

    
    def playMusic(self, volume):
        """ Plays tutorial music on loop infinitely at the given volume """
        if self.music != None:
            self.music.set_volume(volume)
            self.music.play(-1)
    
    def stopMusic(self):
        if self.music != None:
            self.music.stop()
    

    def exit(self):
        if super().getObj("xButton").getPressed():
            self.stopMusic()
            return True
            
        return False


    def update(self, window):
        """ Updates left/right buttons"""
        super().update(window)