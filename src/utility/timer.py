import logging

class Timer:
    def __init__(self, delay):
        """ Sets up delay and timer variables"""
        self.log = logging.getLogger(__name__)

        self.delay = delay
        self.timer = delay

        self.activate = False
    
    
    def activated(self, window):
        """ Updates timer and resets if it reached the end, returns True if activated """
        self.update(window)
        self.activate = self.overActivated()
        return self.activate

        
    def update(self, window):
        """ Decrements timer by the amount of time that has passed since the last frame """
        self.timer -= window.getDeltaTime()


    def overActivated(self):
        """ For low FPS, if there's still time left on the timer (as in,
            if the FPS is so low the timer has activated several times in one frame),
            remove the excess time once and return True """
        if self.timer <= 0:
            self.timer += self.delay
            return True

        return False
    

    def changeDelay(self, newDelay):
        self.delay = newDelay
    

    def getPercentDone(self):
        """ Returns a decimal for the percent that the timer is done """
        return ( self.delay - self.timer ) / self.delay
    
    def getActivate(self):
        return self.activate
    
    def getDelay(self): return self.delay
    def getTimeLeft(self): return self.timer

    def setToEnd(self): self.timer = 0