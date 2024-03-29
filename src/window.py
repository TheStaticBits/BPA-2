import pygame
import logging

import time

from src.utility.vector import Vect
from src.ui.error import Error
import src.utility.utility as util 

class Window:
    """ Handles window and inputs """
    def __init__(self, constants):
        """ Creates window and variables for keeping track of inputs """
        self.log = logging.getLogger(__name__)
        
        self.log.info("Creating window")

        try:
            self.window = pygame.display.set_mode(constants["window"]["size"])
        
        except KeyError as exc:
            Error.createError("Unable to find window size data in the constants JSON file. Defaulting to (800, 600).", 
                              self.log, exc, recoverable=True)
            self.window = pygame.display.set_mode((800, 600))

        self.close = False
        

        try:
            pygame.display.set_caption(constants["window"]["title"])
        
        except KeyError as exc:
            Error.createError("Unable to find window tile in the constants JSON file. Defaulting to \"Game\".",
                              self.log, exc, recoverable=True)
            pygame.display.set_caption("Game")
        
        try:
            icon = util.loadTexTransparent(constants["window"]["icon"])
            pygame.display.set_icon(icon)
        
        except KeyError as exc:
            Error.createError("Unable to find the icon path in constants.json", self.log, exc, recoverable=True)
        

        try:
            self.outputFPS = constants["window"]["outputFPS"]
                
        except KeyError as exc:
            Error.createError("Unable to find window outputFPS data within constants JSON file. Defaulting to no FPS output.", self.log, exc)
            self.outputFPS = False
        

        try:
            self.maxFPS = constants["window"]["maxFPS"]
        
        except KeyError as exc:
            Error.createError("Unable to find window max FPS data within constants JSON file. Defaulting to no FPS cap.", self.log, exc)
            self.maxFPS = False
        

        try:
            self.speedupIcon = util.loadTexTransparent(constants["misc"]["speedup"]["icon"])
            self.speedupPos = Vect(constants["misc"]["speedup"]["pos"])
        
        except KeyError as exc:
            Error.createError("Unable to find speedup icon information in constants JSON file.", self.log, exc)


        self.clock = pygame.time.Clock()

        self.mousePos = (0, 0)
        self.mousePressed =  { "left": False, "right": False }
        self.mouseReleased = { "left": False, "right": False }
        
        self.escapePressed = False

        self.prevTime = time.time() # seconds
        self.deltaTime = 0

        self.FPSTimer = self.prevTime
        self.pastSecondFPS = []
        self.speedup = False


    def update(self, constants):
        """ Updates the display with what has been rendered in the past frame
            and cap FPS """
        
        pygame.display.flip() # Update display
        self.window.fill((0, 0, 0)) # Clear the window with black
        
        
        # update delta time, seconds since last frame
        # Any movement will be multiplied by this, making any movement 
        # move at the same speed regardless of framerate 
        self.deltaTime = time.time() - self.prevTime
        self.prevTime = time.time()

        if self.speedup:
            self.deltaTime *= 2

        # FPS tracker
        if self.outputFPS:
            if self.deltaTime != 0:
                self.pastSecondFPS.append(1 / self.deltaTime)

            if self.prevTime >= self.FPSTimer:
                self.FPSTimer += 1

                # average
                fpsAverage = 0 
                for fps in self.pastSecondFPS: fpsAverage += fps
                fpsAverage /= len(self.pastSecondFPS)

                if self.speedup:
                    # Accounting for double the game speed in order to show actual FPS
                    fpsAverage *= 2 
                
                self.log.info(f"FPS: {round(fpsAverage)}")
                self.pastSecondFPS.clear()


        # Cap framerate
        if self.maxFPS >= 0:
            self.clock.tick(self.maxFPS)
    
    
    def handleInputs(self):
        """ Handling inputs """
        self.escapePressed = False

        self.mousePos = pygame.mouse.get_pos()

        self.mouseReleased["left"] = False
        self.mouseReleased["right"] = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close = True
            
            # Pressing shift will toggle the doubling of delta time,
            # which doubles the speed of the entire game.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.speedup = not self.speedup
                
                elif event.key == pygame.K_ESCAPE:
                    self.escapePressed = True
                

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click down
                    self.mousePressed["left"] = True
                elif event.button == 3: # right click down
                    self.mousePressed["right"] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left click up
                    self.mousePressed["left"] = False
                    self.mouseReleased["left"] = True
                elif event.button == 3: # right click up
                    self.mousePressed["right"] = False
                    self.mouseReleased["right"] = True

    
    def render(self, tex, pos):
        """ Render a texture to the window at pos """
        self.window.blit(tex, pos.getTuple())
    

    def renderSpeedupIcon(self):
        """ Renders speedup icon in the top right if 2x speedup mode is active """
        if self.speedup:
            self.render(self.speedupIcon, self.speedupPos)
    

    # Getters
    def getMouse(self, button): return self.mousePressed[button]
    def getMouseReleased(self, button): return self.mouseReleased[button]
    def getMousePos(self): return Vect(self.mousePos)
    
    def getEscapeKey(self): return self.escapePressed

    def getDeltaTime(self): return self.deltaTime

    def isClosed(self): return self.close