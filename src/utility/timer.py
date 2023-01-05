import logging

class Timer:
    def __init__(self, delay):
        """ Sets up delay and timer variables"""
        self.log = logging.getLogger(__name__)

        self.delay = delay
        self.timer = delay
        
        self.activate = False
    
    
    def update(self, window):
        """ Updates timer and resets if it reached the end """
        self.activate = False

        self.timer -= window.getDeltaTime()

        if self.timer <= 0:
            self.timer += self.delay
            self.activate = True
    

    def activated(self): 
        return self.activate
    

    def changeDelay(self, newDelay):
        self.delay = newDelay
    

    def getPercentDone(self):
        """ Returns a decimal for the percent that the timer is done """
        return ( self.delay - self.timer ) / self.delay