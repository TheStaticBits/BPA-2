import pygame
import logging

import src.entities.tower as tower

class OneEnemyTower(tower.Tower):
    """ Overrides tower attack, attacks one enemy in the range at a time """
    def __init__(self, type, towersJson):
        super().__init__(self, type, towersJson)
    
    


class AllEnemiesTower(tower.Tower):
    """ Attacks all enemies in the range for each attack """
    pass

class NuclearTower(tower.Tower):
    """ Hits one enemy, spawns an attack circle around that enemy and
        deals damage to enemies in the range around the first selected enemy """
    pass