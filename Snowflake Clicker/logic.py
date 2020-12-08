"""________________________________________________________________
-------------------------------------------------------------------
Program:        logic.py
Author:         Tyler Jusczak
Version :       1.0
Purpose:

___________________________________________________________________
-------------------------------------------------------------------"""
import pygame
import math
import time

class Logic(object):

    def __init__(self):
        pygame.init()
        self.starttime = time.time()

        self.flake = 0

        #Main Snowflake
        self.sfClick   = 1
        self.sfCurrent = 0
        self.sfTotal   = 0
        self.sfQueue   = 0
        self.sfAdd     = 0
        self.sfps      = 0

        #Upgrades
        self.autoSpin = False

        self.mainClickLevel = 0
        self.snowmanLevel = 1
        self.cookieLevel = 1
        self.deerLevel = 1
        self.santaLevel = 1

        # Snowman
        self.snowmanCount = 0
        self.snowmanProduction = 0.1
        self.snowmanCost = 15
        self.snowmanCostGrowth = 1.15
        self.snowmanFPS = self.snowmanCount * self.snowmanProduction * self.snowmanLevel
        self.snowmanFlakesMade = 0

        # Cookie
        self.cookieCount = 0
        self.cookieProduction = 1
        self.cookieCost = 100
        self.cookieCostGrowth = 1.15
        self.cookieFPS = self.cookieCount * self.cookieProduction * self.cookieLevel
        self.cookieFlakesMade = 0

        # Deer
        self.deerCount = 0
        self.deerProduction = 8
        self.deerCost = 1100
        self.deerCostGrowth = 1.15
        self.deerFPS = self.deerCount * self.deerProduction * self.deerLevel
        self.deerFlakesMade = 0
        # Santa
        self.santaCount = 0
        self.santaProduction = 47
        self.santaCost = 12000
        self.santaCostGrowth = 1.15
        self.santaFPS = self.santaCount * self.santaProduction * self.santaLevel
        self.santaFlakesMade = 0
    # Main snow button
    def snowButtonClicked(self):
        self.sfCurrent += self.sfClick
        self.sfTotal += self.sfClick

    # Buy Functions
    def snowmanBuy(self):
        if self.sfCurrent >= self.snowmanCost:
            self.sfCurrent -= self.snowmanCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.snowmanCount += 1
            self.snowmanCost = round(self.snowmanCost * self.snowmanCostGrowth)

    def cookieBuy(self):
        if self.sfCurrent >= self.cookieCost:
            self.sfCurrent -= self.cookieCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.cookieCount += 1
            self.cookieCost = round(self.cookieCost * self.cookieCostGrowth)

    def deerBuy(self):
        if self.sfCurrent >= self.deerCost:
            self.sfCurrent -= self.deerCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.deerCount += 1
            self.deerCost = round(self.deerCost * self.deerCostGrowth)

    def santaBuy(self):
        if self.sfCurrent >= self.santaCost:
            self.sfCurrent -= self.santaCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.santaCount += 1
            self.santaCost = round(self.santaCost * self.santaCostGrowth)

    # Updating
    def snowmanUpdate(self):
        self.snowmanFPS = round(self.snowmanCount * self.snowmanProduction * self.snowmanLevel,2)
        self.snowmanFlakesMade += self.snowmanFPS
        self.snowmanFlakesMade = round(self.snowmanFlakesMade)
        self.sfQueue += self.snowmanFPS

    def cookieUpdate(self):
        self.cookieFPS = round(self.cookieCount * self.cookieProduction * self.cookieLevel,2)
        self.cookieFlakesMade += self.cookieFPS
        self.cookieFlakesMade = round(self.cookieFlakesMade)
        self.sfQueue += self.cookieFPS

    def deerUpdate(self):
        self.deerFPS = round(self.deerCount * self.deerProduction * self.deerLevel,2)
        self.deerFlakesMade += self.deerFPS
        self.deerFlakesMade = round(self.deerFlakesMade)
        self.sfQueue += self.deerFPS

    def santaUpdate(self):
        self.santaFPS = round(self.santaCount * self.santaProduction * self.santaLevel,2)
        self.santaFlakesMade += self.santaFPS
        self.santaFlakesMade = round(self.santaFlakesMade)
        self.sfQueue += self.santaFPS

    def update(self):

        if self.snowmanCount > 0:
            self.snowmanUpdate()
        if self.cookieCount > 0:
            self.cookieUpdate()
        if self.deerCount > 0:
            self.deerUpdate()
        if self.santaCount > 0:
            self.santaUpdate()

        if self.sfQueue >= 1:
            self.sfAdd = self.sfQueue
            self.sfAdd = round(self.sfQueue)
            self.sfQueue -= self.sfAdd
            self.sfCurrent += self.sfAdd
            self.sfTotal += self.sfAdd
            self.flake = self.sfAdd
            self.sfAdd = 0

        self.sfps = round(self.snowmanFPS + self.cookieFPS + self.deerFPS + self.santaFPS, 2)
