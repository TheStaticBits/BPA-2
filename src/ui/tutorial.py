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
        
        self.slide = 0 # slide number in the tutorial
        
        # Finds the number of slides that exist in the UI data
        self.amountOfSlides = 0
        while super().objExists(str(self.amountOfSlides)): # tests if that slide exists
            self.amountOfSlides += 1
        
        self.changeSlides() # Updates to the initial slide

    
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
    
    
    def changeSlides(self):
        """ Sets the objects in the slide to render while setting everything else to not """
        # Sets all slides to not display
        for slide in range(self.amountOfSlides):
            # Set the slide to display if it is the current slide, otherwise set it to not display
            super().getObj(str(slide)).setDisplaying(slide == self.slide)

            # Iterates through all objects
            for name, obj in super().getAllObjects().items():
                # Tests if the object's first character in its name is the slide number
                if name[0] == str(slide):
                    # If the slide is the one to display, set to display, otherwise set to not
                    obj.setDisplaying(slide == self.slide)


    def update(self, window):
        """ Updates left/right buttons"""
        super().update(window)

        if super().getObj("left").getPressed():
            self.slide -= 1
            if self.slide < 0: self.slide = self.amountOfSlides - 1
            self.changeSlides()
        
        elif super().getObj("right").getPressed():
            self.slide += 1
            if self.slide >= self.amountOfSlides: self.slide = 0
            self.changeSlides()