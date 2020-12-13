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
import os
import pickle
import time

class Logic(object):

    def __init__(self):
        pygame.init()

        # Time Tracking
        self.timeRunningSec = 0
        self.timeRunningMin = 0
        self.timeRunningHour = 0
        self.lastSave = ""

        #Main Snowflake
        self.sfClick   = 1
        self.sfTimesClicked = 0
        self.sfAmountFromClicks = 0
        self.sfCurrent = 0
        self.sfTotal   = 0
        self.sfQueue   = 0
        self.sfAdd     = 0
        self.sfps      = 0
        self.flake     = 0 # Used for making snowflakes

        self.autoSpinPurchased = False
        self.autoSpinOn = False

        # Snowman
        self.snowmanCount = 0
        self.snowmanLevel = 1
        self.snowmanProduction = 0.1
        self.snowmanCost = 15
        self.snowmanCostGrowth = 1.15
        self.snowmanLevelCostTrack = [0,100,500,5000,20000,50000,100000,400000,1000000,5000000,20000000,0]
        self.snowmanLevelCost = self.snowmanLevelCostTrack[self.snowmanLevel]
        self.snowmanFPS = self.snowmanCount * self.snowmanProduction
        self.snowmanFlakesMade = 0

        # Cookie
        self.cookieCount = 0
        self.cookieLevel = 1
        self.cookieProduction = 1
        self.cookieCost = 100
        self.cookieCostGrowth = 1.15
        self.cookieLevelCostTrack = [0,1000,6000,30000,100000,500000,2000000,5000000,20000000,50000000,150000000,0]
        self.cookieLevelCost = self.cookieLevelCostTrack[self.cookieLevel]
        self.cookieFPS = self.cookieCount * self.cookieProduction
        self.cookieFlakesMade = 0

        # Deer
        self.deerCount = 0
        self.deerLevel = 1
        self.deerProduction = 8
        self.deerCost = 1100
        self.deerCostGrowth = 1.15
        self.deerLevelCostTrack = [0,10000,30000,60000,200000,1000000,5000000,15000000,50000000,200000000,500000000,0]
        self.deerLevelCost = self.deerLevelCostTrack[self.deerLevel]
        self.deerFPS = self.deerCount * self.deerProduction
        self.deerFlakesMade = 0
        # Santa
        self.santaCount = 0
        self.santaLevel = 1
        self.santaProduction = 47
        self.santaCost = 12000
        self.santaCostGrowth = 1.15
        self.santaLevelCostTrack = [0, 100000,300000,600000,1500000,3000000,10000000,30000000,100000000,500000000,1500000000,40000000000,0]
        self.santaLevelCost = self.santaLevelCostTrack[self.santaLevel]
        self.santaFPS = self.santaCount * self.santaProduction
        self.santaFlakesMade = 0

    # Main snow button
    def snowButtonClicked(self):
        self.sfCurrent += self.sfClick
        self.sfTotal += self.sfClick
        self.sfTimesClicked += 1
        self.sfAmountFromClicks += self.sfClick

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

    # Level Up Functions
    def snowmanLevelUp(self):
        if self.sfCurrent >= self.snowmanLevelCost:
            self.sfCurrent -= self.snowmanLevelCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.snowmanLevel += 1
            # Levels up Clicking snowflake also
            self.sfClick = self.sfClick * 2
            self.snowmanLevelCost = self.snowmanLevelCostTrack[self.snowmanLevel]
            self.snowmanProduction = self.snowmanProduction * 2

    def cookieLevelUp(self):
        if self.sfCurrent >= self.cookieLevelCost:
            self.sfCurrent -= self.cookieLevelCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.cookieLevel += 1
            self.cookieLevelCost = self.cookieLevelCostTrack[self.cookieLevel]
            self.cookieProduction = self.cookieProduction * 2

    def deerLevelUp(self):
        if self.sfCurrent >= self.deerLevelCost:
            self.sfCurrent -= self.deerLevelCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.deerLevel += 1
            self.deerLevelCost = self.deerLevelCostTrack[self.deerLevel]
            self.deerProduction = self.deerProduction * 2

    def santaLevelUp(self):
        if self.sfCurrent >= self.santaLevelCost:
            self.sfCurrent -= self.santaLevelCost
            self.sfCurrent = round(self.sfCurrent, 2)
            self.santaLevel += 1
            self.santaLevelCost = self.santaLevelCostTrack[self.santaLevel]
            self.santaProduction = self.santaProduction * 2

    # Updating
    def snowmanUpdate(self):
        self.snowmanFPS = round(self.snowmanCount * self.snowmanProduction,2)
        self.snowmanFlakesMade += self.snowmanFPS
        self.snowmanFlakesMade = round(self.snowmanFlakesMade)
        self.sfQueue += self.snowmanFPS

    def cookieUpdate(self):
        self.cookieFPS = round(self.cookieCount * self.cookieProduction,2)
        self.cookieFlakesMade += self.cookieFPS
        self.cookieFlakesMade = round(self.cookieFlakesMade)
        self.sfQueue += self.cookieFPS

    def deerUpdate(self):
        self.deerFPS = round(self.deerCount * self.deerProduction,2)
        self.deerFlakesMade += self.deerFPS
        self.deerFlakesMade = round(self.deerFlakesMade)
        self.sfQueue += self.deerFPS

    def santaUpdate(self):
        self.santaFPS = round(self.santaCount * self.santaProduction,2)
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

        if self.autoSpinOn == True:
            self.sfCurrent += self.sfClick
            self.sfTotal += self.sfClick

        self.sfps = round(self.snowmanFPS + self.cookieFPS + self.deerFPS + self.santaFPS, 2)
        self.timeRunningSec += 1
        if self.timeRunningSec == 60:
            self.timeRunningMin += 1
            self.timeRunningSec = 0
        if self.timeRunningMin == 60:
            self.timeRunningHour += 1
            self.timeRunningMin = 0
