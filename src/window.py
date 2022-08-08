import pygame
import logging

log = logging.getLogger(__name__)

class Window:
    """ Handles window and inputs """
    def __init__(self, constants):
        """ Creates window and variables for keeping track of inputs """
        
        self.window = pygame.display.set_mode(constants["window"]["size"])
        self.close = False
        
        pygame.display.set_caption(constants["window"]["title"])
        
        self.clock = pygame.time.Clock()
        
        self.inputs = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.keys = {
            "up": (pygame.K_UP, pygame.K_w),
            "down": (pygame.K_DOWN, pygame.K_s),
            "left": (pygame.K_LEFT, pygame.K_a),
            "right": (pygame.K_RIGHT, pygame.K_d)
        }

        self.mousePos = (0, 0)
        self.mousePressed = {}

    def update(self, constants):
        """ Updates the display with what has been rendered in the past frame
            and cap FPS """
        
        pygame.display.flip() # Update display
        self.window.fill((0, 0, 0)) # Clear the window with black

        # Cap framerate
        if constants["window"]["maxFPS"] != 0:
            self.clock.tick(constants["window"]["maxFPS"])
    
    def handle_inputs(self):
        """ Handling inputs """
        self.mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close = True
            
            elif event.type == pygame.KEYUP:
                for key in self.keys:
                    if event.type in self.keys[key]:
                        self.inputs[key] = False
                        
            elif event.type == pygame.KEYDOWN:
                for key in self.keys:
                    if event.type in self.keys[key]:
                        self.inputs[key] = True