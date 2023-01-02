import pygame
import logging

import src.utility.utility as util
from src.entities.enemy import Enemy
from src.utility.vector import Vect
from src.ui.error import Error
from src.utility.timer import Timer

class Waves:
    """ Handles waves interpreter and stores enemies """

    def __init__(self, consts):
        """ Load waves JSON and other creationary stuff"""
        self.log = logging.getLogger(__name__)

        try:
            self.wavesJson = util.loadJson(consts["jsonPaths"]["waves"])
            self.enemiesJson = util.loadJson(consts["jsonPaths"]["enemies"])

        except KeyError as exc:
            Error.createError("Unable to find JSON path data for waves or enemies.", self.log, exc)
            return None
        

        try:
            self.health = consts["game"]["playerHealth"]
        
        except KeyError as exc:
            Error.createError("Unable to find player health data within the constants JSON file.", self.log, exc)
            return None


        self.waveNum = 0
        self.waveDelay = Timer(self.getWaveDelay())
        self.enemies = []
        self.drops = {}

        self.updateSpawnData(0)
    

    def updateSpawnData(self, waveNum):
        """ Creates data dictionary for spawning enemies"""
        self.spawnData = {}
        try:
            for enemy, data in self.wavesJson[waveNum]["enemies"].items():
                self.spawnData[enemy] = { "amountLeft": data["amount"],
                                          "delay": Timer(data["startDelay"]) }

        except KeyError as exc:
            Error.createError(f"Unable to find wave enemy data for the wave {waveNum} in the waves JSON file.", self.log, exc)
    

    def update(self, window, tileset):
        """ Update enemies and delays, and creates enemies """
        
        self.drops = { "wood": 0, "steel": 0, "uranium": 0 }
        
        stillAlive = []
        for enemy in self.enemies:
            enemy.update(window, tileset)
            
            if enemy.hasReachedMapEnd(tileset):
                self.health -= enemy.getDamage() # player take damage
                # self.log.info(f"Player health now at {self.health}")
            
            elif not enemy.isDead(tileset): # Enemy alive still
                stillAlive.append(enemy)
            
            else: # Enemy died
                drops = enemy.getDrops()
                
                # adding drops to the current frame's drops
                for drop, amount in drops.items():
                    self.drops[drop] += amount
            
        self.enemies = stillAlive
        
        if len(self.spawnData) == 0: # Test for new wave
            self.waveDelay.update(window) # Delay timer for delay between waves

            if self.waveDelay.activated(): # Start next wave
                self.waveNum += 1

                if self.waveNum >= len(self.wavesJson):
                    self.log.error("Reached the end of the waves?? Oops!")
                    self.waveNum = 0
                
                self.updateSpawnData(self.waveNum)

            else:
                return None # no need to update spawning enemies when delaying between waves


        # Update wave delays and spawn any enemies
        for enemy, data in self.spawnData.items():
            data["delay"].update(window)

            if data["delay"].activated(): 
                # Reset delay and spawn enemy
                try:
                    data["delay"].changeDelay(self.wavesJson[self.waveNum]["enemies"][enemy]["spawnDelay"])
                
                except KeyError as exc:
                    Error.createError("Unable to find enemy spawn data in the waves JSON file.", self.log, exc)
                    return None

                data["amountLeft"] -= 1
                self.enemies.append(Enemy(enemy, tileset, self.enemiesJson))
        
        # Removes anything that has finished spawning enemies
        self.spawnData = { enemy: data for enemy, data in self.spawnData.items() if data["amountLeft"] > 0 }
            
    
    def render(self, window):
        """ Renders enemies """
        for enemy in self.enemies:
            enemy.render(window)
    

    def getCollided(self, img, pos):
        """ Returns a list of enemies that collide pixel perfect with the given img """
        collided = []

        for enemy in self.enemies:
            enemyImg, enemyPos = enemy.getAnim().getImgFrame(), enemy.getPos()

            # Testing rectangle collision first,
            # to save performance on the costly pixel perfect collision
            if util.rectCollision(pos1=Vect(enemyPos), size1=Vect(enemyImg.get_size()),
                                  pos2=pos, size2=Vect(img.get_size())):
                                  
                if util.pixelPerfectCollision(img1=img, pos1=pos, img2=enemyImg, pos2=enemyPos):
                    collided.append(enemy)
        
        return collided
    

    def getFrameDrops(self): return self.drops # Enemy drops from that frame
    def getWaveNum(self): return self.waveNum
    def getWaveDelay(self): 
        try:
            return self.wavesJson[self.waveNum]["delay"]
        except KeyError as exc:
            Error.createError(f"Unable to find wave delay number for wave {self.waveNum}.", self.log, exc)