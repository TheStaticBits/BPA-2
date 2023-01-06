import pygame
import logging
import random

import src.utility.utility as util
from src.entities.entity import Entity
from src.utility.timer import Timer
from src.utility.vector import Vect
from src.ui.error import Error
from src.utility.advDict import AdvDict

class Enemy(Entity):
    """ Any enemies are inherited from this class.
        Handles enemy movement and enemy animations. """

    # Moving: ------------ Left ------- Up -------- Right ----- Down
    DIR_CLOCKWISE = [ Vect(-1, 0), Vect(0, -1), Vect(1, 0), Vect(0, 1) ]

    def __init__(self, type, tileset, enemiesJson):
        self.log = logging.getLogger(__name__)

        self.reachedEnd = False
        self.showFlash = False
        self.showFlashTimer = None
        
        try:
            self.speed =  enemiesJson[type]["speed"]
            self.health = enemiesJson[type]["health"]

            self.dropAmount =  enemiesJson[type]["dropAmount"]
            self.dropChances = enemiesJson[type]["dropChances"]

            self.flashColor = enemiesJson["damageFlashColor"]
            self.flashExtensionWidth = enemiesJson["damageFlashSizeExtention"]
            self.showFlashTime = enemiesJson["damageFlashTime"]
            
            animData = enemiesJson[type]["animation"]

            if "ability" in enemiesJson[type]:
                self.ability = enemiesJson[type]["ability"]["execute"]
                self.abilityTimer = Timer(enemiesJson[type]["ability"]["delay"])
            else:
                self.ability = None
        
        except KeyError as exc:
            Error.createError(f"Unable to find the following required data value within the Enemy JSON file for the {type} enemy.", self.log, exc)
            return None

        startPos = tileset.getEnemyStartPos()

        try:
            # Gets start tile
            startTile = tileset.getTileAt(Vect(startPos["tile"]))
            self.moveDir = Vect(startPos["facingDir"])
        except KeyError as exc:
            Error.createError(f"Unable to find required tile data within the tiles JSON file for the start position of the {type} enemy.", self.log, exc)
            return None
        
        self.nextTile = startTile.getCoords() # Moving to start tile from offscreen

        super().__init__(animData) # sets up animation 
        
        # Position offscreen, moving onto the start tile
        pos = self.getPosOnTile(startTile) - (self.moveDir * startTile.getSize())
        super().setPos(pos) # setup position
    

    def getDamageFlashImg(self):
        """ 
        Creates an image slightly larger than the enemy, drawing the enemy image four times 
        in each corner of the larger image, and then sets the entire image to the damage flash
        color.
        """

        frame = super().getAnim().getImgFrame()
        frameSize = Vect(frame.get_size())

        # Creates image flashExtentionWidth pixels wider in each direction than the original
        damageFlash = pygame.Surface((frameSize + self.flashExtensionWidth * 2).getTuple(), flags=pygame.SRCALPHA)

        # Drawing the image in the four corners of the image
        # Iterates through x and y for each corner
        for x in range(0, self.flashExtensionWidth * 2 + 1 , self.flashExtensionWidth * 2):
            for y in range(0, self.flashExtensionWidth * 2 + 1, self.flashExtensionWidth * 2): 
                damageFlash.blit(frame, (x, y))
        
        # Turning the outline to the damage outline color
        color = pygame.Surface(damageFlash.get_size())
        color.fill(self.flashColor)

        # Multiplies alphas, leaving a solid color silhouette
        damageFlash.blit(color, (0, 0), special_flags=pygame.BLEND_PREMULTIPLIED)

        # Set transparency of the flash to correspond with how much time is left showing the flash
        damageFlash.set_alpha((1 - self.showFlashTimer.getPercentDone()) * 255)

        return damageFlash


    def update(self, window, tileset):
        """ Updates animation and position of enemy """
        super().updateAnim(window)

        # Move
        super().addToPos(self.moveDir * (self.speed * window.getDeltaTime()))
        
        # Reached the next tile destination
        onTile = tileset.getTileAt(self.nextTile)
        if self.onNextTile(window, onTile): # turn to next tile and set dest

            super().setPos(self.getPosOnTile(onTile)) # center on tile
            self.turn(onTile.getMoveDir())
            
            # moving destination by one board coordinate
            self.nextTile = onTile.getCoords() + self.moveDir
        
        self.updateAbility(window)

        # Update outline timer
        if self.showFlash:
            self.showFlashTimer.update(window)

            if self.showFlashTimer.activated(): # Show outline ended
                self.showFlash = False
    

    def updateAbility(self, window):
        """ Updates ability timer if there is one """
        if self.ability != None:
            self.abilityTimer.update(window)

            if self.abilityTimer.activated():
                exec(self.ability) 
    

    def onNextTile(self, window, tile):
        """ Tests if the enemy has reached the next tile """
        
        if tile == False: # Moved off board
            self.reachedEnd = True
            return False
        
        # Finding difference in x/y between the tile and where it needs to move to
        diff = (self.getPosOnTile(tile) - super().getPos()).abs()

        # amount moved per frame
        frameDistance = self.speed * window.getDeltaTime()

        # Tile within one frame of movement from the destination
        return diff.x <= frameDistance and diff.y <= frameDistance
    
    
    def turn(self, direction):
        """ Implements turning left, right, and turning around """
        index = self.DIR_CLOCKWISE.index(self.moveDir)

        if direction == "forward": return None      # No turning
        elif direction == "right":       index += 1 # Clockwise
        elif direction == "left":        index -= 1 # Counterclockwise
        elif direction == "turn around": index += 2 # Turn around

        # Wrap around the list, end or start
        if index >= len(self.DIR_CLOCKWISE): 
            index -= len(self.DIR_CLOCKWISE)
        elif index < 0: 
            index = len(self.DIR_CLOCKWISE) - 1
        
        self.moveDir = self.DIR_CLOCKWISE[index]
    

    def takeDamage(self, amount):
        """ Enemy takes damage of amount """
        self.health -= amount
        self.showFlash = True # Shows damage outline for a small period of time
        self.showFlashTimer = Timer(self.showFlashTime)
    
    
    def getPosOnTile(self, tile):
        return tile.getCenter() - (super().getAnim().getSize() / 2)
    

    def hasReachedMapEnd(self, tileset):
        """ Returns true if the enemy has moved off the screen """
        if not self.reachedEnd: return False

        # Check if on board
        return not util.rectCollision(super().getPos(), super().getAnim().getSize(),
                                      Vect(0, 0),       tileset.getBoardSize())
    
    def isDead(self, tileset):
        """ Returns true if the enemy has died """
        return self.health <= 0

    def getDamage(self):
        return self.health
        # Damage done to the player's health upon reaching the end,
        # the health remaining on the enemy is dealt to the player's health as 

    
    def getDrops(self):
        """ Returns a dictionary of how much of each resource the enemy dropped """
        drops = AdvDict({}) # Empty adv dictionary

        for i in range(self.dropAmount):
            num = random.randint(0, 100)

            # Matches up the random number with a drop chance and 
            # adds one drop to the resource randomly chosen
            for resource, chance in self.dropChances.items():
                if resource not in drops: # Set initial value for the resource in drops
                    drops[resource] = 0
                
                if num <= chance: # Chosen resource!
                    drops[resource] += 1
                    break
                else:
                    num -= chance # Moving onto the next resource's chances
        
        return drops
    

    def render(self, window):
        """ Renders enemy and red flash if taking damage """
        super().render(window)

        if self.showFlash:
            window.render(self.getDamageFlashImg(), super().getPos() - Vect(self.flashExtensionWidth))