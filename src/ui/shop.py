import pygame
import logging

from src.ui.ui import UI
from src.ui.button import Button

class Shop(UI):
    def __init__(self, consts, uiData):
        super().__init__(True)

        super().load(consts, "shop", uiData)
    

    def update(self, window, money):
        """ Handles button events and shop-related updates """
        super().update(window)

        # Updates amount of money displayed
        for name, amount in money.items():
            obj = super().getObj(name + "Txt")
            obj.changeText(str(amount))

    
    def render(self, window):
        """ Handles shop-specific rendering events """
        super().render(window)