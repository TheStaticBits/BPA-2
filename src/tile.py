import pygame
import logging

import src.utility as util
import src.animation as anim
import src.entity as entity
from src.vector import Vect

class Tile:
    """ Handles each tile and the images and functionality """
    
    textures = {} # Dict, {tileTypeChar: pygame.Surface} 

    def __init__(self, type, coord, tileJson):
        """ Setup tile """
        self.log = logging.getLogger(__name__)
        
        self.coord = Vect(coord)

        self.loadTileData(type, tileJson)
        self.loadTex(tileJson)

        self.mouseOnTile = False
        self.hoverOffset = 0

        # Coordinates given multiplied by the tile size
        # (position on screen)
        self.pos = Vect(coord) * self.textures[self.type].get_width()

        if self.hasDeco:
            # Setup decoration centered at offset
            pos = (self.pos + self.decoOffset - (self.deco.getAnim().getSize() // 2))
            self.deco.setPos(pos)

    
    def loadTileData(self, type, tileJson):
        """ Loads data for the tile into variables, 
            including tile decorations if any, and more """
        self.hasDeco = type in tileJson["deco"]
        self.rotate = None

        if self.hasDeco:
            self.type = tileJson["deco"][type]["tile"] # Tile type of the tile behind deco
            self.decoTile = type
            self.decoOffset = Vect(tileJson["deco"][type]["offset"])
            self.isPlacable = tileJson["deco"][type]["placable"]

            animData = tileJson["deco"][type]["animation"]
            self.deco = entity.Entity(animData)

        else:
            if type in tileJson["rotated"]:
                self.rotate = tileJson["rotated"][type]["degrees"]
                type = tileJson["rotated"][type]["tile"]
            
            if type not in tileJson["tiles"]:
                self.log.error(f"Tile \"{type}\" not declared in tiles.json")
            
            self.type = type
            self.move = tileJson["tiles"][type]["move"]
            
                
    def loadTex(self, tileJson):
        """ Loads texture into class variable if it hasn't already been loaded """
        
        if self.type not in self.textures:
            # load and add tex to class variable textures, for future
            # tiles of the same type
            path = tileJson["tiles"][self.type]["path"]
            self.textures[self.type] = util.loadTexTransparent(path)
    

    def updateMouseHover(self, window, consts):
        """ Updates tile moving up and down when mouse hovers over it """

        if self.canBePlacedOn():
            # Tile will not move upon hovering
            return None

        if util.pointRectCollision(window.getMousePos(), self.pos, Vect(self.getWidth())):
            # The chin/shadow under the square tile height
            moveTo = self.getHeight() - self.getWidth()
            # slowly moves to moveTo
            self.hoverOffset += consts["game"]["tileHoverSpeed"] * window.getDeltaTime() * (moveTo - self.hoverOffset)
        else:
            if self.hoverOffset < 0.5:
                self.hoverOffset = 0
            else:
                # Move down to zero
                self.hoverOffset -= consts["game"]["tileHoverSpeed"] * window.getDeltaTime() * self.hoverOffset


    def update(self, window, consts):
        """ Updates tile hovering, deco animations """
        if self.hasDeco: 
            self.deco.updateAnim(window)

        self.updateMouseHover(window, consts)

    
    def render(self, window): # window is the Window object
        """ Render the tile itself """ 
        tex = self.textures[self.type]

        if self.rotate != None: 
            tex = pygame.transform.rotate(tex, self.rotate)

        renderPos = self.pos.copy()
        renderPos.y -= self.hoverOffset
        
        window.render(tex, renderPos)
    
    
    def renderDeco(self, window):
        """ Renders the decoration at the offset if there's any deco """
        if self.hasDeco: self.deco.render(window)
    

    # Getters
    def getMoveDir(self):
        """ Gets enemy move direction for the tile """
        return False if self.hasDeco else self.move

    def getCenter(self):
        """ Returns center of tile position """ 
        return self.pos + (self.getSize() // 2)
    
    def getSize(self):   return Vect(self.textures[self.type].get_size())
    def getWidth(self):  return self.getSize().x
    def getHeight(self): return self.getSize().y

    def getCoord(self): return self.coord
    def getPos(self):   return self.pos

    def canBePlacedOn(self): return (self.hasDeco and not self.isPlacable) or self.move != "none"