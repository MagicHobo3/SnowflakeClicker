"""________________________________________________________________
-------------------------------------------------------------------
Program:        gui.py
Author:         Tyler Jusczak
Version :       1.0
Purpose:

___________________________________________________________________
-------------------------------------------------------------------"""
import pygame
import random
import pickle
import os
from datetime import datetime
from guiElements import Text, Button, Panel, ToolTip, CircleGrowAnim

class GUI(object):

    def __init__(self, width, height, logic):
        pygame.init()
        pygame.font.init()

        # COLORS
        self.COLORS = {"CLICKEDCOLOR" : (110,123,165), "HIGHLIGHTCOLOR" : (161, 163, 172),"MAINCOLOR" : (63, 65, 70),
                       "TEXTCOLOR" : (255, 255, 255) , "BLACK" : (11,13,17), "RED" : (236,72,72),
                       "DARKGREEN" : (53, 80, 51), "BUTTONRED" : (236,72,72),"SNOW" : (255,255,255)}

        self.FONTS = {"TEXTFONT"    : pygame.font.SysFont('freestyle script', 35),
                      "SMALLFONT"   : pygame.font.SysFont('freestyle script', 25),
                      "HUGEFONT"    : pygame.font.SysFont('freestyle script', 80),
                      "BIGFONT"     : pygame.font.SysFont('freestyle script', 40),
                      "BUTTONFONT"  : pygame.font.SysFont('freestyle script', 30)}

        self.logic = logic
        self.text   = Text()
        self.button = Button()
        self.toolTip = ToolTip()


        self.my = 0
        self.mx = 0

        self.mouseDown = False
        self.oneClick  = False

        self.currentSong = "Music/Wish Background.mp3"

        self.width   = width
        self.height  = height
        self.screen  = pygame.display.set_mode((width,height))
        self.caption = pygame.display.set_caption("Snowflake Clicker")
        self.icon    = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(self.icon)

        # Background Image
        self.bgimg         = "assets/background.jpg"
        self.bg            = pygame.image.load(self.bgimg)
        self.bgRect        = self.bg.get_rect()
        self.bgRect.center = width//2, height//2

        # Main Snowflake Button
        self.snowflakeImg   = "assets/mainFlake.png"
        self.sfImg          = pygame.image.load(self.snowflakeImg)
        self.sfImgAngle     = 0
        self.sfSpeed        = 0
        self.sfMaxSpeed     = 3
        self.sfAccel        = 0.3
        self.sfFriction     = 0.04
        self.sfRect         = self.sfImg.get_rect()
        self.sfRect.center  = 200, 400
        self.snowBackCircle = []
        for circle in range(0,2):
            self.snowBackCircle.append(CircleGrowAnim(self.screen, self.sfRect.center[0], self.sfRect.center[1], self.COLORS["BUTTONRED"], 100 ,110 - circle * 20))



        # Main Snowflake Inner Circle
        self.sfInnerCircleImg         = pygame.image.load("assets/inner.png")
        self.sfInnerCircleImgAngle    = 0
        self.sfInnerCircleSpeed       = 0
        self.sfInnerCircleMaxSpeed    = 2
        self.sfInnerCircleAccel       = 0.2
        self.sfInnerCircleFriction    = 0.05
        self.sfInnerCircleRect        = self.sfInnerCircleImg.get_rect()
        self.sfInnerCircleRect.center = 200, 400

        # Main Snowflake Outer Circle
        self.sfOuterCircleImg         = pygame.image.load("assets/outer.png")
        self.sfOuterCircleImgAngle    = 0
        self.sfOuterCircleSpeed       = 0
        self.sfOuterCircleMaxSpeed    = 2.5
        self.sfOuterCircleAccel       = 0.35
        self.sfOuterCircleFriction    = 0.05
        self.sfOuterCircleRect        = self.sfOuterCircleImg.get_rect()
        self.sfOuterCircleRect.center = 200, 400

        # Falling Flake
        self.fallingFlakeImg = "assets/fall.png"
        self.ffImg           = pygame.image.load(self.fallingFlakeImg)
        self.ffRect          = self.ffImg.get_rect()
        self.ffRect.center   = 0, 0
        self.flakeFallSpeed  = 2
        self.allFlakes       = {}

        # Snowman Icons
        self.snowmanImg    = "assets/Icons/snowman.png"
        self.smImg         = pygame.image.load(self.snowmanImg)
        self.smRect        = self.smImg.get_rect()
        self.smRect.center = 1000, 200

        self.snowmanSmallImg    = "assets/Items/snowman.png"
        self.smSmallImg         = pygame.image.load(self.snowmanSmallImg)
        self.smSmallRect        = self.smSmallImg.get_rect()
        self.smSmallRect.center = 840, 60

        # Cookie Icons
        self.cookieImg    = "assets/Icons/cookie.png"
        self.cImg         = pygame.image.load(self.cookieImg)
        self.cRect        = self.cImg.get_rect()
        self.cRect.center = 1000, 325

        self.cookieSmallImg    = "assets/Items/cookie.png"
        self.cSmallImg         = pygame.image.load(self.cookieSmallImg)
        self.cSmallRect        = self.cImg.get_rect()
        self.cSmallRect.center = 930, 50

        # Deer Icons
        self.deerImg      = "assets/Icons/deer.png"
        self.dImg         = pygame.image.load(self.deerImg)
        self.dRect        = self.dImg.get_rect()
        self.dRect.center = 1000, 465

        self.deerSmallImg      = "assets/Items/deer.png"
        self.dSmallImg         = pygame.image.load(self.deerSmallImg)
        self.dSmallRect        = self.dSmallImg.get_rect()
        self.dSmallRect.center = 1020, 50

        # Santa Icons
        self.santaImg     = "assets/Icons/santa.png"
        self.sImg         = pygame.image.load(self.santaImg)
        self.sRect        = self.sImg.get_rect()
        self.sRect.center = 1000, 601

        self.santaSmallImg     = "assets/Items/santa.png"
        self.sSmallImg         = pygame.image.load(self.santaSmallImg)
        self.sSmallRect        = self.sSmallImg.get_rect()
        self.sSmallRect.center = 1110, 60


        # Button Vars
        self.statsOpen   = False
        self.optionsOpen = False
        self.infoOpen    = False

    def drawBackground(self):
        self.screen.blit(self.bg, self.bgRect)

    """ MAIN SNOWFLAKE BUTTON """
    def snowButton(self):

        # Main snowflake and rings spin when its speed is > 0 . Then slow speed by friction amount.
        if self.sfSpeed > 0:
            self.sfImgAngle += self.sfSpeed
            self.sfSpeed    -= self.sfFriction

        if self.sfOuterCircleSpeed > 0:
            self.sfOuterCircleImgAngle += self.sfOuterCircleSpeed
            self.sfOuterCircleSpeed    -= self.sfOuterCircleFriction

        if self.sfInnerCircleSpeed > 0:
            self.sfInnerCircleImgAngle += self.sfInnerCircleSpeed
            self.sfInnerCircleSpeed -= self.sfOuterCircleFriction

        # Creating a number between 0 and 255 based on the percentage of spin of the outer ring.
        hueShiftDown = 255 - (255 * (self.sfOuterCircleSpeed / self.sfOuterCircleMaxSpeed))
        if hueShiftDown < 40:
            hueShiftDown = 40
        if hueShiftDown > 255:
            hueShiftDown = 255
        hueShiftUp = (255 * (self.sfOuterCircleSpeed / self.sfOuterCircleMaxSpeed))
        if hueShiftUp < 40:
            hueShiftUp = 40
        if hueShiftUp > 255:
            hueShiftUp = 255

        # Using the hue shift values, self.colorize recreates the image with a diffrent color.
        self.sfImgColored = self.colorize(self.sfImg, (hueShiftUp,hueShiftUp,hueShiftUp))
        self.innerCircleColored = self.colorize(self.sfInnerCircleImg, (255,hueShiftDown,hueShiftDown))
        self.outerCircleColored = self.colorize(self.sfOuterCircleImg, (hueShiftDown,255,hueShiftDown))

        # Now that the color is set, self.rotateCenter creates a copy of that image again.
        # rotates it and sets the center to the orignal image center. To create the spin effect.
        snowButtonSurface = self.rotateCenter(self.sfImgColored, self.sfImgAngle, self.sfRect.center)
        innerCircleSurface = self.rotateCenter(self.innerCircleColored, self.sfInnerCircleImgAngle, self.sfInnerCircleRect.center)
        outerCircleSurface = self.rotateCenter(self.outerCircleColored, self.sfOuterCircleImgAngle, self.sfOuterCircleRect.center)

        # Finally draw the final image to the screen.
        self.screen.blit(outerCircleSurface[0], outerCircleSurface[1])
        self.screen.blit(innerCircleSurface[0], innerCircleSurface[1])
        self.screen.blit(snowButtonSurface[0], snowButtonSurface[1])

    """ FALLING FLAKES """
    def newFlake(self):
        """Create a new snowflake in the dictionary and give it a random Y value"""
        if len(self.allFlakes) > 0:
            lastID = int(list(self.allFlakes.keys())[-1])
        else:
            lastID = 0
        newFlakeID = str(lastID + 1)

        self.allFlakes[newFlakeID] =  {"x":random.randint(0, 1200), "y":0, "speed" : random.randint(3,6)}

    def drawFlakes(self):
        """For each snowflake in the list, move postion and draw to screen"""
        if len(self.allFlakes) > 0:
            for key in self.allFlakes:

                self.allFlakes[key]["y"] += self.allFlakes[key]["speed"]
                newCenterY = self.allFlakes[key]["y"]

                self.ffRect.center = self.allFlakes[key]["x"], newCenterY
                self.screen.blit(self.ffImg, self.ffRect.center)

            # Delete snowflake from Dict if off screen
            for key in self.allFlakes:
                if self.allFlakes[key]["y"] > self.height + 50:
                    self.allFlakes.pop(key)
                    break

    """ HUD ToolTips, PANELS, ICONS"""
    def drawHUD(self):
        optionPanel = pygame.Rect(400,0,400,80)
        pygame.draw.rect(self.screen, self.COLORS["BLACK"], optionPanel)

        topRight = pygame.Surface((1200,800))
        topRightRect = pygame.Rect(0,0,400,400)
        topRight.set_colorkey((0,0,0))
        topRight.set_alpha(200)
        pygame.draw.rect(topRight, self.COLORS["BLACK"],topRightRect)

        buySurface = pygame.Surface((1200,800))
        buyRect = pygame.Rect(800,0,400,800)
        buySurface.set_colorkey((0,0,0))
        buySurface.set_alpha(200)
        pygame.draw.rect(buySurface, self.COLORS["BLACK"],buyRect)

        # Snowman Buy Bar & Tool Tip
        snowmanToolTip = Panel(self.screen, 800, 180,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        snowmanBackground = Panel(self.screen, 800, 180,400,120, self.COLORS["SNOW"], alpha = 50)


        snowmanTipText1 = "SNOWMAN"
        snowmanTipText2 = (str(self.logic.snowmanCount) + " snowmen, making " + str(self.logic.snowmanFPS) + " flakes per second")
        snowmanTipText3 = ("Total flakes made by snowmen : " + str(self.logic.snowmanFlakesMade))

        if(self.mx > snowmanToolTip.getRect()[0] and self.mx < snowmanToolTip.getRect()[0] + snowmanToolTip.getRect()[2] and
           self.my > snowmanToolTip.getRect()[1] and self.my < snowmanToolTip.getRect()[1] + snowmanToolTip.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, snowmanBackground.getRect(), (255,255,255), self.FONTS["SMALLFONT"], snowmanTipText1, snowmanTipText2, snowmanTipText3)

        # Cookie Buy Bar & Tool Tip
        cookieToolTip = Panel(self.screen, 800, 320,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        cookieBackground = Panel(self.screen, 800, 320,400,120, self.COLORS["SNOW"], alpha = 50)

        cookieTipText1 = "GINGERBREAD COOKIE"
        cookieTipText2 = (str(self.logic.cookieCount) + " cookies, making " + str(self.logic.cookieFPS) + " flakes per second")
        cookieTipText3 = ("Total flakes made by cookies : " + str(self.logic.cookieFlakesMade))

        if(self.mx > cookieToolTip.getRect()[0] and self.mx < cookieToolTip.getRect()[0] + cookieToolTip.getRect()[2] and
           self.my > cookieToolTip.getRect()[1] and self.my < cookieToolTip.getRect()[1] + cookieToolTip.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, cookieBackground.getRect(), (255,255,255), self.FONTS["SMALLFONT"], cookieTipText1, cookieTipText2, cookieTipText3)

        # Deer Buy Bar & Tool Tip
        deerToolTip = Panel(self.screen, 800, 460,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        deerBackground = Panel(self.screen, 800, 460,400,120, self.COLORS["SNOW"], alpha = 50)

        deerTipText1 = "REINDEER"
        deerTipText2 = (str(self.logic.deerCount) + " reindeer, making " + str(self.logic.deerFPS) + " flakes per second")
        deerTipText3 = ("Total flakes made by reindeer : " + str(self.logic.deerFlakesMade))

        if(self.mx > deerToolTip.getRect()[0] and self.mx < deerToolTip.getRect()[0] + deerToolTip.getRect()[2] and
           self.my > deerToolTip.getRect()[1] and self.my < deerToolTip.getRect()[1] + deerToolTip.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, deerBackground.getRect(), (255,255,255), self.FONTS["SMALLFONT"], deerTipText1, deerTipText2, deerTipText3)

        # Santa Buy Bar & Tool Tip
        santaToolTip = Panel(self.screen, 800, 600,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        santaBackground = Panel(self.screen, 800, 600,400,120, self.COLORS["SNOW"], alpha = 50)

        santaTipText1 = "SANTA"
        santaTipText2 = (str(self.logic.santaCount) + " santas, making " + str(self.logic.santaFPS) + " flakes per second")
        santaTipText3 = ("Total flakes made by santas : " + str(self.logic.santaFlakesMade))

        if(self.mx > santaToolTip.getRect()[0] and self.mx < santaToolTip.getRect()[0] + santaToolTip.getRect()[2] and
           self.my > santaToolTip.getRect()[1] and self.my < santaToolTip.getRect()[1] + santaToolTip.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, santaBackground.getRect(), (255,255,255), self.FONTS["SMALLFONT"], santaTipText1, santaTipText2, santaTipText3)

        self.screen.blit(buySurface, (0,0))
        snowmanBackground.drawPanel()
        cookieBackground.drawPanel()
        deerBackground.drawPanel()
        santaBackground.drawPanel()

        snowmanToolTip.drawPanel()
        cookieToolTip.drawPanel()
        deerToolTip.drawPanel()
        santaToolTip.drawPanel()
        self.screen.blit(topRight, (0,0))
        self.screen.blit(self.smSmallImg, self.smSmallRect.center)
        self.screen.blit(self.cSmallImg, self.cSmallRect.center)
        self.screen.blit(self.dSmallImg, self.dSmallRect.center)
        self.screen.blit(self.sSmallImg, self.sSmallRect.center)
        self.screen.blit(self.smImg, self.smRect.center)
        self.screen.blit(self.cImg, self.cRect.center)
        self.screen.blit(self.dImg, self.dRect.center)
        self.screen.blit(self.sImg, self.sRect.center)

    """ HUD TEXT """
    def drawText(self):

        """ Snowflake Total Text """
        self.text.makeText(self.screen,'Snowflakes : ' + str(self.logic.sfCurrent), self.COLORS["TEXTCOLOR"], self.FONTS["BIGFONT"], (200, 90))

        """ Snowflake Per Second Text """
        self.text.makeText(self.screen, 'Per Second : ' + str(self.logic.sfps), self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (200, 130))

        """ Snowflake Click Amount Text """
        self.text.makeText(self.screen, 'SF Per Click : ' + str(self.logic.sfClick), self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (200, 180))

        """ Level Up Text """
        self.text.makeText(self.screen, " Level Up | 2x Flakes Per Second", self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (1000, 25))

        """ Snowman Count """
        self.text.makeText(self.screen, str(self.logic.snowmanCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,240))

        """ Cookie Count """
        self.text.makeText(self.screen, str(self.logic.cookieCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,380))

        """ Deer Count """
        self.text.makeText(self.screen, str(self.logic.deerCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,520))

        """ Santa Count """
        self.text.makeText(self.screen, str(self.logic.santaCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,660))

        """ Tool Tip Zone text """
        self.text.makeText(self.screen,'?', self.COLORS["BLACK"], self.FONTS["TEXTFONT"], (825, 240))
        self.text.makeText(self.screen,'?', self.COLORS["BLACK"], self.FONTS["TEXTFONT"], (825, 380))
        self.text.makeText(self.screen,'?', self.COLORS["BLACK"], self.FONTS["TEXTFONT"], (825, 520))
        self.text.makeText(self.screen,'?', self.COLORS["BLACK"], self.FONTS["TEXTFONT"], (825, 660))

    """ HUD BUTTONS """
    def drawButtons(self):

        """ Stats Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               "STATS", pygame.Rect(421,20,90,40), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.statsToggle)
        if self.statsOpen == True:
            self.statsButtonFunc()

        """ Option Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               "OPTIONS", pygame.Rect(560,20,90,40), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.optionsToggle)
        if self.optionsOpen == True:
            self.optionsButtonFunc()

        """ Info Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               "INFO", pygame.Rect(690,20,90,40), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.infoToggle)
        if self.infoOpen == True:
            self.infoButtonFunc()

        """ Auto Spin Button """
        if self.logic.autoSpinPurchased == False:
            self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                   "Autospin / Autoclick = 1 Million ", pygame.Rect(10,700,400,60), self.COLORS["MAINCOLOR"],
                                   self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"],
                                   self.buyAutoSpin)
        else:
            if self.logic.autoSpinOn == True:
                self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                       "Autospin Toggle", pygame.Rect(10,700,400,60), self.COLORS["RED"],
                                       self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"],
                                       self.autoSpinToggle)
            else:
                self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                       "Autospin Toggle", pygame.Rect(10,700,400,60), self.COLORS["MAINCOLOR"],
                                       self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"],
                                       self.autoSpinToggle)

        """ Snowman Button """
        # Buy
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               self.numbercondenser(str(self.logic.snowmanCost)), pygame.Rect(930,215,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.snowmanBuyFunc)

        # Level Up
        if self.logic.snowmanLevel < 10:
            self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                   self.numbercondenser(str(self.logic.snowmanLevelCost)), pygame.Rect(825,110,80,30), self.COLORS["MAINCOLOR"],
                                   self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                                   self.snowmanLevelUpFunc)
            self.text.makeText(self.screen, str(self.logic.snowmanLevel) + " / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (875,160))
        else:
            self.text.makeText(self.screen, "MAX", self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (875,125))
            self.text.makeText(self.screen, "10 / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (875,160))

        """ Cookie Button """
        # Buy
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               self.numbercondenser(str(self.logic.cookieCost)), pygame.Rect(930,355,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.cookieBuyFunc)
        # Level Up
        if self.logic.cookieLevel < 10:
            self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                self.numbercondenser(str(self.logic.cookieLevelCost)), pygame.Rect(915,110,80,30), self.COLORS["MAINCOLOR"],
                                self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                                self.cookieLevelUpFunc)
            self.text.makeText(self.screen, str(self.logic.cookieLevel) + " / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (955,160))
        else:
            self.text.makeText(self.screen, "MAX", self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (955,125))
            self.text.makeText(self.screen, "10 / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (955,160))

        """ Deer Button """
        # Buy
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               self.numbercondenser(str(self.logic.deerCost)), pygame.Rect(930,495,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.deerBuyFunc)
        # Level Up
        if self.logic.deerLevel < 10:
            self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                   self.numbercondenser(str(self.logic.deerLevelCost)), pygame.Rect(1005,110,80,30), self.COLORS["MAINCOLOR"],
                                   self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                                   self.deerLevelUpFunc)
            self.text.makeText(self.screen, str(self.logic.deerLevel) + " / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (1045,160))
        else:
            self.text.makeText(self.screen, "MAX", self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (1045,125))
            self.text.makeText(self.screen, "10 / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (1045,160))


        """ Santa Button """
        # Buy
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               self.numbercondenser(str(self.logic.santaCost)), pygame.Rect(930,635,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.santaBuyFunc)
        # Level Up
        if self.logic.santaLevel < 10:
            self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                                self.numbercondenser(str(self.logic.santaLevelCost)), pygame.Rect(1095,110,80,30), self.COLORS["MAINCOLOR"],
                                self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                                self.santaLevelUpFunc)
            self.text.makeText(self.screen, str(self.logic.santaLevel) + " / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (1135,160))
        else:
            self.text.makeText(self.screen, "MAX", self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (1135,125))
            self.text.makeText(self.screen, "10 / 10", self.COLORS["TEXTCOLOR"], self.FONTS["SMALLFONT"], (1135,160))

    def numbercondenser(self, startingCost):
        text = 0

        if len(startingCost) < 4:
            text = startingCost
        elif len(startingCost) == 4:
            text = startingCost[0] + "." + startingCost[1] + "k"
        elif len(startingCost) == 5:
            text = startingCost[0] + startingCost[1] + "." + startingCost[2] + "k"
        elif len(startingCost) == 6:
            text = startingCost[0] + startingCost[1] + startingCost[2] + "." + startingCost[3] + "k"
        elif len(startingCost) == 7:
            text = startingCost[0] + "." + startingCost[1] + "m"
        elif len(startingCost) == 8:
            text = startingCost[0] + startingCost[1] + "." + startingCost[2] + "m"
        elif len(startingCost) == 9:
            text = startingCost[0] + startingCost[1] + startingCost[2] + "." + startingCost[3] + "m"
        elif len(startingCost) == 10:
            text = startingCost[0] + "." + startingCost[1] + "b"
        elif len(startingCost) == 11:
            text = startingCost[0] + startingCost[1] + "." + startingCost[2] + "b"
        elif len(startingCost) == 12:
            text = startingCost[0] + startingCost[1] + startingCost[2] + "." + startingCost[3] + "b"
        elif len(startingCost) == 13:
            text = startingCost[0] + "." + startingCost[1] + "t"
        elif len(startingCost) == 14:
            text = startingCost[0] + startingCost[1] + "." + startingCost[2] + "t"
        elif len(startingCost) == 15:
            text = startingCost[0] + startingCost[1] + startingCost[2] + "." + startingCost[3] + "t"
        else:
            text = startingCost

        return str(text)

    # Used for buy and level up buttons
    def snowmanBuyFunc(self):
        if self.oneClick == True:
            self.logic.snowmanBuy()
            self.oneClick = False
    def snowmanLevelUpFunc(self):
        if self.oneClick == True:
            self.logic.snowmanLevelUp()
            self.oneClick = False

    def cookieBuyFunc(self):
        if self.oneClick == True:
            self.logic.cookieBuy()
            self.oneClick = False
    def cookieLevelUpFunc(self):
        if self.oneClick == True:
            self.logic.cookieLevelUp()
            self.oneClick = False

    def deerBuyFunc(self):
        if self.oneClick == True:
            self.logic.deerBuy()
            self.oneClick = False
    def deerLevelUpFunc(self):
        if self.oneClick == True:
            self.logic.deerLevelUp()
            self.oneClick = False

    def santaBuyFunc(self):
        if self.oneClick == True:
            self.logic.santaBuy()
            self.oneClick = False
    def santaLevelUpFunc(self):
        if self.oneClick == True:
            self.logic.santaLevelUp()
            self.oneClick = False

    # Functions for buying auto spin
    def buyAutoSpin(self):
        if self.logic.sfCurrent >= 1000000:
            self.logic.autoSpinPurchased = True
            self.logic.autoSpinOn = True
    def autoSpinToggle(self):
        if self.logic.autoSpinOn == False:
            self.logic.autoSpinOn = True
        else:
            self.logic.autoSpinOn = False

    # These toggle functions keep the button from being pressed twice with one click
    def statsToggle(self):
        if self.statsOpen == False and self.oneClick == True:
            self.statsOpen = True
            self.oneClick = False
        elif self.statsOpen == True and self.oneClick == True:
            self.statsOpen = False
            self.oneClick = False

    def optionsToggle(self):
        if self.optionsOpen == False and self.oneClick == True:
            self.optionsOpen = True
            self.oneClick = False
        elif self.optionsOpen == True and self.oneClick == True:
            self.optionsOpen = False
            self.oneClick = False

    def infoToggle(self):
        if self.infoOpen == False and self.oneClick == True:
            self.infoOpen = True
            self.oneClick = False
        elif self.infoOpen == True and self.oneClick == True:
            self.infoOpen = False
            self.oneClick = False

    def statsButtonFunc(self):
        # Toggle Other Button Menus to close
        self.optionsOpen = False
        self.infoOpen = False

        # Main Button Highlight
        pygame.draw.line(self.screen, self.COLORS["RED"], (421,60), (510,60), 6)

        # Main Panel
        statsPanel = Panel(self.screen, 400, 80, 400, 800, self.COLORS["BLACK"], 200)
        statsPanel.drawPanel()

        # Text for stats panel
        self.text.makeText(self.screen, "Time Since Start : " + str(self.logic.timeRunningHour) + ":" + str(self.logic.timeRunningMin) + ":" + str(self.logic.timeRunningSec), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-350))
        self.text.makeText(self.screen, "Total snowflakes made : " + str(self.logic.sfTotal), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-300))
        self.text.makeText(self.screen, "Snowflakes Hand Made : " + str(self.logic.sfAmountFromClicks), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-250))
        self.text.makeText(self.screen, "Snowflake Clicked : " + str(self.logic.sfTimesClicked), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-200))

        self.text.makeText(self.screen, "Snowman FPS: " + str(self.logic.snowmanFPS), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-100))
        self.text.makeText(self.screen, "Cookie FPS: " + str(self.logic.cookieFPS), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-50))
        self.text.makeText(self.screen, "Reindeer FPS: " + str(self.logic.deerFPS), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,0))
        self.text.makeText(self.screen, "Santa FPS: " + str(self.logic.santaFPS), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,50))

        self.text.makeText(self.screen, "Per Snowman : " + str(self.logic.snowmanProduction), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,100))
        self.text.makeText(self.screen, "Per Cookie : " + str(self.logic.cookieProduction), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,150))
        self.text.makeText(self.screen, "Per Reindeer : " + str(self.logic.deerProduction), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,200))
        self.text.makeText(self.screen, "Per Santa : " + str(self.logic.santaProduction), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,250))

    def optionsButtonFunc(self):
        # Toggle Other Button Menus to close
        self.statsOpen = False
        self.infoOpen = False

        # Main Button Highlight
        pygame.draw.line(self.screen, self.COLORS["RED"], (560,60), (649,60), 6)

        # Main Panel
        optionsPanel = Panel(self.screen, 400, 80, 400, 800, self.COLORS["BLACK"], 200)
        optionsPanel.drawPanel()

        # Save
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "Save", pygame.Rect(550,100,100,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.pickle)
        self.text.makeText(self.screen, "Last Save: " + str(self.logic.lastSave), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], (600,150))


        # Volume change Buttons
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "Volume Up", pygame.Rect(500,200,200,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.volumeUp)
        self.text.makeText(self.screen, str(round(pygame.mixer.music.get_volume() * 10) ) + " / 10", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], optionsPanel.getCenter(0,-220))
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "Volume Down", pygame.Rect(500,300,200,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.volumeDown)

        # Music Change Buttons
        self.text.makeText(self.screen, "Change Music", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], optionsPanel.getCenter(0,-50))
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "Wish Background", pygame.Rect(450,500,300,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.changeMusicWish)
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "Canon Variation", pygame.Rect(450,550,300,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.changeMusicCanon)
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "Deck The Halls", pygame.Rect(450,600,300,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.changeMusicDeck)
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "O Holy Night", pygame.Rect(450,650,300,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.changeMusicHoly)
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                            "We Wish You A Merry Christmas", pygame.Rect(450,700,300,30), self.COLORS["MAINCOLOR"],
                            self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                            self.changeMusicMerry)

        # Music Button Highlighting
        if self.currentSong == "Music/Wish Background.mp3":
            pygame.draw.line(self.screen, self.COLORS["RED"], (450,500), (450,529), 10)
        elif self.currentSong == "Music/Canon and Variation.mp3":
            pygame.draw.line(self.screen, self.COLORS["RED"], (450,550), (450,579), 10)
        elif self.currentSong == "Music/Deck the Halls A.mp3":
            pygame.draw.line(self.screen, self.COLORS["RED"], (450,600), (450,629), 10)
        elif self.currentSong == "Music/Oh Holy Night.mp3":
            pygame.draw.line(self.screen, self.COLORS["RED"], (450,650), (450,679), 10)
        elif self.currentSong == "Music/We Wish You A Merry Christmas.mp3":
            pygame.draw.line(self.screen, self.COLORS["RED"], (450,700), (450,729), 10)

    def infoButtonFunc(self):
        # Toggle Other Button Menus to close
        self.statsOpen = False
        self.optionsOpen = False

        # Main Button Highlight
        pygame.draw.line(self.screen, self.COLORS["RED"], (690,60), (779,60), 6)

        # Main Panel
        infoPanel = Panel(self.screen, 400, 80, 400, 800, self.COLORS["BLACK"], 200)
        infoPanel.drawPanel()

        # Text for info panel
        self.text.makeText(self.screen, "* Snowflake Clicker *", self.COLORS["SNOW"], self.FONTS["BIGFONT"], infoPanel.getCenter(0,-250))
        self.text.makeText(self.screen, "Created by Tyler A Jusczak", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], infoPanel.getCenter(0,-200))
        self.text.makeText(self.screen, "Dec, 2020", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], infoPanel.getCenter(0,-160))

        self.text.makeText(self.screen, "This project was a lot of fun to make", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], infoPanel.getCenter(0,-100))
        self.text.makeText(self.screen, "and I learned so much in the process.", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], infoPanel.getCenter(0,-50))
        self.text.makeText(self.screen, "Thanks for Playing", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], infoPanel.getCenter(0,0))
        self.text.makeText(self.screen, "and", self.COLORS["SNOW"], self.FONTS["TEXTFONT"], infoPanel.getCenter(0,50))
        self.text.makeText(self.screen, "MERRY CHRISTMAS!", self.COLORS["SNOW"], self.FONTS["BIGFONT"], infoPanel.getCenter(0,100))

    def volumeUp(self):
        volume = round(pygame.mixer.music.get_volume(),2)
        if volume < 1:
            volume += 0.1
            pygame.mixer.music.set_volume(volume)
        if volume > 1:
            volume = 1
            pygame.mixer.music.set_volume(volume)

    def volumeDown(self):
        volume = round(pygame.mixer.music.get_volume(),2)
        if volume > 0:
            volume -= 0.1
            pygame.mixer.music.set_volume(volume)
        if volume < 0:
            volume = 0
            pygame.mixer.music.set_volume(volume)

    def changeMusicWish(self):
        if self.currentSong != "Music/Wish Background.mp3":
            self.currentSong = "Music/Wish Background.mp3"
            pygame.mixer.music.load("Music/Wish Background.mp3")
            pygame.mixer.music.play(-1)

    def changeMusicCanon(self):
        if self.currentSong != "Music/Canon and Variation.mp3":
            self.currentSong = "Music/Canon and Variation.mp3"
            pygame.mixer.music.load("Music/Canon and Variation.mp3")
            pygame.mixer.music.play(-1)

    def changeMusicDeck(self):
        if self.currentSong != "Music/Deck the Halls A.mp3":
            self.currentSong = "Music/Deck the Halls A.mp3"
            pygame.mixer.music.load("Music/Deck the Halls A.mp3")
            pygame.mixer.music.play(-1)

    def changeMusicHoly(self):
        if self.currentSong != "Music/Oh Holy Night.mp3":
            self.currentSong = "Music/Oh Holy Night.mp3"
            pygame.mixer.music.load("Music/Oh Holy Night.mp3")
            pygame.mixer.music.play(-1)

    def changeMusicMerry(self):
        if self.currentSong != "Music/We Wish You A Merry Christmas.mp3":
            self.currentSong = "Music/We Wish You A Merry Christmas.mp3"
            pygame.mixer.music.load("Music/We Wish You A Merry Christmas.mp3")
            pygame.mixer.music.play(-1)


        """ GENERIC FUNCTIONS """
    def rotateCenter(self, image, angle, center):
        """Rotate the image and keep original center point"""
        rotatedImage = pygame.transform.rotate(image, angle)
        rotateImageRect = rotatedImage.get_rect(center=center)

        return rotatedImage, rotateImageRect

    def colorize(self, image, newColor):
        image = image.copy()

        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

        return image

    def autoSpin(self):
        if self.logic.autoSpinOn == True:
            self.sfSpeed = self.sfMaxSpeed
            self.sfInnerCircleSpeed = self.sfInnerCircleMaxSpeed
            self.sfOuterCircleSpeed = self.sfOuterCircleMaxSpeed

    def pickle(self):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        self.logic.lastSave = date_time
        save = open('savedata.txt', "wb")
        pickle.dump(self.logic, save)
        save.close()
        print("Saved Progress : " + str(date_time))


    def update(self):
        if self.logic.flake > 0:
            self.newFlake()
            self.logic.flake -= 1
        self.drawFlakes()
        self.drawHUD()
        self.drawButtons()
        self.drawText()
        pygame.draw.ellipse(self.screen, self.COLORS["BLACK"], self.sfOuterCircleRect)
        for back in self.snowBackCircle:
            back.update()
        self.snowButton()
        self.autoSpin()

        pygame.display.update()
