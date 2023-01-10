import pygame
import logging

import src.utility.utility as util
from src.entities.entity import Entity
from src.utility.vector import Vect
from src.ui.error import Error

class Tile:
    """ Handles each tile and the images and functionality """
    
    textures = {} # Dict, { tilesetName: {tileTypeChar: pygame.Surface} } 

    def __init__(self, type, coords, tileJson):
        """ Setup tile """
        self.log = logging.getLogger(__name__)
        
        self.coords = coords

        try: # Try loading and setting up variables using data from the tile's JSON file
            self.loadTileData(type, tileJson)

        except KeyError as exc:
            Error.createError(f"Unable to find required data to load the tile data for the tile {type}", self.log, exc)
            return None
            
        
        try: # Try loading tile image using data from the tile's JSON file
            self.loadTex(tileJson)

        except KeyError as exc:
            Error.createError(f"Unable to find required data to load the image for the tile {type}", self.log, exc)
            return None

        self.mouseOnTile = False
        self.hoverOffset = 0
        
        self.hasTower = False

        # Coordinates given multiplied by the tile size
        # (position on screen)
        self.pos = coords * self.textures[self.tilesetName][self.type].get_width()

        if self.hasDeco:
            # Setup decoration centered at offset
            pos = (self.pos + self.decoOffset - (self.deco.getAnim().getSize() // 2))
            self.deco.setPos(pos)

    
    def loadTileData(self, type, tileJson):
        """ Loads data for the tile into variables, 
            including tile decorations if any, and more """
        self.hasDeco = type in tileJson["deco"]
        self.rotate = None
        self.unmovable = False
        self.tilesetName = tileJson["name"]

        if self.hasDeco: # Decoration tile, has to load animation on tile and stuff
            self.type = tileJson["deco"][type]["tile"] # Tile type of the tile behind deco
            self.decoTile = type
            self.decoOffset = Vect(tileJson["deco"][type]["offset"])
            self.unmovable = not tileJson["deco"][type]["placable"]
            self.moveWithTile = tileJson["deco"][type]["moveWithTile"]

            animData = tileJson["deco"][type]["animation"]
            self.deco = Entity(animData)

        else:
            # Tile that is a rotated version of a normal tile
            if type in tileJson["rotated"]:
                self.rotate = tileJson["rotated"][type]["degrees"]
                self.type = tileJson["rotated"][type]["tile"]
                
                if "move" in tileJson["rotated"][type]:
                    self.move = tileJson["rotated"][type]["move"]
                else:
                    self.move = tileJson["tiles"][self.type]["move"]

            
            # Tile that can have towers placed on it
            else: 
                if type in tileJson["unmovable"]:
                    type = tileJson["unmovable"][type]["tile"]
                    self.unmovable = True
                
                self.move = tileJson["tiles"][type]["move"]
                self.type = type
            
                
    def loadTex(self, tileJson):
        """ Loads texture into class variable if it hasn't already been loaded """
        
        if self.tilesetName not in self.textures:
            self.textures[self.tilesetName] = {}

        self.loadTile(self.type, tileJson)

        # loading base tile
        self.baseTile = tileJson["baseTile"]
        self.loadTile(self.baseTile, tileJson)
    

    def loadTile(self, tile, tileJson):
        """ If the tile is not loaded yet, load it and store in cache for the future """
        if tile not in self.textures[self.tilesetName]:
            # load and add tex to class variable textures, for future
            # tiles of the same type
            path = tileJson["tiles"][tile]["path"]
            self.textures[self.tilesetName][tile] = util.loadTexTransparent(path)
    

    def updateMouseHover(self, window, consts):
        """ Updates tile moving up and down when mouse hovers over it """

        self.mouseOnTile = util.pointRectCollision(window.getMousePos(), self.pos, Vect(self.getWidth()))

        if not self.canBePlacedOn():
            # Tile will not move upon hovering
            return None

        if self.mouseOnTile and not window.getMouse("left"):
            # The chin/shadow under the square tile height
            moveTo = self.getHeight() - self.getWidth()
            # slowly moves to moveTo
            self.hoverOffset += consts["game"]["tileHoverSpeed"] * window.getDeltaTime() * (moveTo - self.hoverOffset)

            if self.hoverOffset > moveTo: self.hoverOffset = moveTo

        else:
            if self.hoverOffset < 0.5:
                self.hoverOffset = 0
            else:
                # Move down to zero
                self.hoverOffset -= consts["game"]["tileHoverSpeed"] * window.getDeltaTime() * self.hoverOffset


    def update(self, window, consts, updateAnim):
        """ Updates tile hovering, deco animations """
        if self.hasDeco: 
            self.deco.updateAnim(window)

        if updateAnim:
            self.updateMouseHover(window, consts)

    
    def render(self, window, surf=False): # window is Window object or an image (if surf is True)
        """ Render the tile itself """ 
        tex = self.textures[self.tilesetName][self.type]

        if self.type != self.baseTile: # Draw base tile below the tile itself
            baseTileImg = self.textures[self.tilesetName][self.baseTile]

            if surf: window.blit(baseTileImg, self.pos.getTuple()) # Draw to an image
            else: window.render(baseTileImg, self.pos) # Draw to the window

        if self.rotate != None: # Rotate if necessary
            tex = pygame.transform.rotate(tex, self.rotate)

        # Applying mouse hover offset
        renderPos = self.pos.copy()
        renderPos.y -= self.hoverOffset
        
        if surf: window.blit(tex, renderPos.getTuple())
        else: window.render(tex, renderPos)
    
    
    def renderDeco(self, window):
        """ Renders the decoration at the offset if there's any deco """
        if self.hasDeco: 
            if self.moveWithTile: 
                self.deco.render(window, yOffset = -self.hoverOffset)
            else:
                self.deco.render(window)
    

    # Getters
    def getMoveDir(self):
        """ Gets enemy move direction for the tile """
        return False if self.hasDeco else self.move

    def getCenter(self):
        """ Returns center of tile position """ 
        return self.pos + (self.getWidth() // 2)
    
    def getSize(self):   return Vect(self.textures[self.tilesetName][self.type].get_size())
    def getWidth(self):  return self.getSize().x
    def getHeight(self): return self.getSize().y

    def getCoords(self): return self.coords
    def getPos(self):   return self.pos

    def getHoverOffset(self): return self.hoverOffset

    def mouseIsOnTile(self): return self.mouseOnTile

    def canBePlacedOn(self): 
        """ Returns true if towers can be placed on the tile """
        if self.unmovable: 
            return False
        elif not self.hasDeco:
            return self.move == "none"
        
        return True

    def getHasTower(self): return self.hasTower
    
    # Setters
    def placedTower(self): self.hasTower = True
    def removeTower(self): self.hasTower = False