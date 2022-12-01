# Run this file to run the game!
import src.game
import pygame

pygame.init()

game = src.game.Game()
game.startLoop()