import pygame
import random
import logging

import src.utility.utility as util
from src.entities.enemy import Enemy
from src.utility.vector import Vect
from src.ui.error import Error
from src.utility.timer import Timer
from src.utility.advDict import AdvDict
from src.particle import Particle

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
        
        # Loading constants.json data
        try:
            self.health = consts["game"]["playerHealth"]
        
        except KeyError as exc:
            Error.createError("Unable to find player health data within the constants JSON file.", self.log, exc)
            return None
        
        try:
            self.particleAmount = consts["game"]["enemyParticleAmount"]
        
        except KeyError as exc:
            Error.createError("Unable to find the enemy death particle amount in constants json.", self.log, exc)


        self.waveNum = 0
        self.waveDelay = Timer(self.getWaveDelay())
        self.enemies = []
        self.particles = []
        self.resources = consts["startingResources"].keys()
        self.drops = AdvDict({})

        self.updateSpawnData(0)
    

    def updateSpawnData(self, waveNum):
        """ Creates data dictionary for spawning enemies"""
        self.log.info(f"Loading wave {waveNum}:")

        self.spawnData = {}
        try:
            for enemy, data in self.wavesJson[waveNum]["enemies"].items():
                self.spawnData[enemy] = { "amountLeft": data["amount"],
                                          "delay": Timer(data["startDelay"]) }
                self.log.info(f"Adding {data['amount']} {enemy} enemies")

        except KeyError as exc:
            Error.createError(f"Unable to find wave enemy data for the wave {waveNum} in the waves JSON file.", self.log, exc)
    

    def update(self, window, tileset, consts):
        """ Update enemies and delays, and creates enemies """
        self.updateEnemies(window, tileset, consts)
        self.updateWaveDelay(window)
        self.spawnEnemies(window, tileset)
        self.updateParticles(window)

        
    def updateEnemies(self, window, tileset, consts):
        """ Updates enemies, detecting when they reach the end of the map or when they die """
        # Makes dictionary with the resources as keys and zero for values 
        self.drops = AdvDict({ key: 0 for key in self.resources })

        stillAlive = []
        for enemy in self.enemies:
            enemy.update(window, tileset)
            
            if enemy.hasReachedMapEnd(tileset):
                self.health -= enemy.getDamage() # player take damage
                self.log.info(f"Player health now at {self.health}")
            
            elif not enemy.isDead(tileset): # Enemy alive still
                stillAlive.append(enemy)
            
            else: # Enemy died
                self.drops += enemy.getDrops()

                self.log.info("Adding enemy death particles")
                for i in range(self.particleAmount):
                    self.particles.append( Particle(consts, enemy.getCenteredPos(), 
                                                    enemy.getAnim().getImgFrame(), 
                                                    random.randint( 0, 359 )) )
            
        self.enemies = stillAlive
    

    def updateWaveDelay(self, window):
        """ Updates the delay between waves """
        if len(self.spawnData) == 0: # Test for new wave
            self.waveDelay.update(window) # Delay timer for delay between waves

            if self.waveDelay.activated(): # Start next wave
                self.waveNum += 1

                if self.waveNum >= len(self.wavesJson):
                    self.log.error("Reached the end of the waves?? Oops!")
                    self.waveNum = 0
                
                self.updateSpawnData(self.waveNum)


    def spawnEnemies(self, window, tileset):
        """ Spawns enemies according to the waves.json file """
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
    

    def updateParticles(self, window):
        """ Updating particles, removing those that are done """
        for particle in self.particles:
            particle.update(window)

        # Keeping particles that are not done
        self.particles = [ particle for particle in self.particles if not particle.isDone() ]
            
    
    def render(self, window):
        """ Renders enemies and particles """
        for enemy in self.enemies:
            enemy.render(window)

        for particle in self.particles:
            particle.render(window)
    

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
    

    def playerIsDead(self): return self.health <= 0
    def getFrameDrops(self): return self.drops # Enemy drops from that frame
    def getWaveNum(self): return self.waveNum
    def getWaveDelay(self): 
        try:
            return self.wavesJson[self.waveNum]["delay"]
        except KeyError as exc:
            Error.createError(f"Unable to find wave delay number for wave {self.waveNum}.", self.log, exc)