import pygame
import logging

import src.utility as util
import src.enemy as en

class Waves:
    """ Handles waves interpreter and stores enemies """

    def __init__(self, consts):
        """ Load waves JSON and other creationary stuff"""
        self.log = logging.getLogger(__name__)

        self.wavesJson = util.loadJson(consts["jsonPaths"]["waves"])
        self.enemiesJson = util.loadJson(consts["jsonPaths"]["enemies"])
        
        self.health = consts["game"]["playerHealth"]
        self.waveNum = 0
        self.waveDelay = 0
        self.enemies = []

        self.updateSpawnData(0)
    

    def updateSpawnData(self, waveNum):
        """ Creates data dictionary for spawning enemies"""
        self.spawnData = {}
        for enemy, data in self.wavesJson[waveNum]["enemies"].items():
            self.spawnData[enemy] = { "amountLeft": data["amount"],
                                      "delay": data["startDelay"] }
    

    def update(self, window, tileset):
        """ Update enemies and delays, and creates enemies """
        
        stillAlive = []
        for enemy in self.enemies:
            enemy.update(window, tileset)
            
            if enemy.hasReachedMapEnd(tileset):
                self.health -= enemy.getDamage() # take damage
                # self.log.info(f"Player health now at {self.health}")
            else:
                stillAlive.append(enemy)
            
        self.enemies = stillAlive
        

        if self.waveDelay > 0:
            self.waveDelay -= window.getDeltaTime()
            return None # No wave to update, currently between waves

        # Update wave delays and spawn any enemies
        for enemy, data in self.spawnData.items():
            data["delay"] -= window.getDeltaTime() 

            if data["delay"] > 0: continue

            # Reset delay and spawn enemy
            data["delay"] = self.wavesJson[self.waveNum]["enemies"][enemy]["spawnDelay"]
            data["amountLeft"] -= 1

            self.enemies.append(en.Enemy(enemy, tileset, self.enemiesJson))
            
        # Removes anything that has finished spawning enemies
        self.spawnData = { enemy: data for enemy, data in self.spawnData.items() if data["amountLeft"] > 0 }

        if len(self.spawnData) == 0: # New WAVE, no more to spawn
            self.waveDelay = self.wavesJson[self.waveNum]["delay"] # delay between waves
            self.waveNum += 1

            if self.waveNum >= len(self.enemiesJson):
                self.log.error("Reached the end of the waves?? Oops!")
            
            self.updateSpawnData(self.waveNum)
            
    
    def render(self, window):
        """ Renders enemies """
        for enemy in self.enemies:
            enemy.render(window)