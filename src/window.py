import pygame
import logging

import time

class Window:
    """ Handles window and inputs """
    def __init__(self, constants):
        """ Creates window and variables for keeping track of inputs """
        self.log = logging.getLogger(__name__)
        
        self.log.info("Creating window")
        self.window = pygame.display.set_mode(constants["window"]["size"])
        self.close = False
        
        pygame.display.set_caption(constants["window"]["title"])
        
        self.clock = pygame.time.Clock()

        self.mousePos = (0, 0)
        self.mousePressed = {}

        self.prevTime = time.time() # seconds
        self.deltaTime = 0


    def update(self, constants):
        """ Updates the display with what has been rendered in the past frame
            and cap FPS """
        
        pygame.display.flip() # Update display
        self.window.fill((0, 0, 0)) # Clear the window with black
        
        # update delta time, seconds since last frame
        # Any movement will be multiplied by this, making any movement 
        # move at the same speed regardless of framerate 
        self.deltaTime = time.time() - self.prevTime

        # Cap framerate
        if constants["window"]["maxFPS"] != 0:
            self.clock.tick(constants["window"]["maxFPS"])
    
    
    def handle_inputs(self):
        """ Handling inputs """
        self.mousePos = pygame.mouse.get_pos()
        
        pressed = pygame.mouse.get_pressed()
        self.mousePressed["left"] =  pressed[0]
        self.mousePressed["right"] = pressed[2]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close = True

    
    # Getters
    def getDeltaTime(self):
        return self.deltaTime