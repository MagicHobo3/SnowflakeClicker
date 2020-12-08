"""________________________________________________________________
-------------------------------------------------------------------
Program:        fui.py
Author:         Tyler Jusczak
Version :       1.0
Purpose:

___________________________________________________________________
-------------------------------------------------------------------"""
import pygame
import random
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
                      "HUGEFONT"    : pygame.font.SysFont('freestyle script', 80),
                      "BIGFONT"     : pygame.font.SysFont('freestyle script', 40),
                      "BUTTONFONT"  : pygame.font.SysFont('freestyle script', 25)}


        self.logic  = logic
        self.text   = Text()
        self.button = Button()
        self.toolTip = ToolTip()


        self.my = 0
        self.mx = 0

        self.mouseDown = False
        self.oneClick  = False

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

        # Snowman Icon
        self.snowmanImg    = "assets/Icons/snowman.png"
        self.smImg         = pygame.image.load(self.snowmanImg)
        self.smRect        = self.smImg.get_rect()
        self.smRect.center = 1000, 200

        # Cookie Icon
        self.cookieImg    = "assets/Icons/cookie.png"
        self.cImg         = pygame.image.load(self.cookieImg)
        self.cRect        = self.cImg.get_rect()
        self.cRect.center = 1000, 325

        # Deer Icon
        self.deerImg      = "assets/Icons/deer.png"
        self.dImg         = pygame.image.load(self.deerImg)
        self.dRect        = self.dImg.get_rect()
        self.dRect.center = 1000, 475

        # Santa Icon
        self.santaImg     = "assets/Icons/santa.png"
        self.sImg         = pygame.image.load(self.santaImg)
        self.sRect        = self.sImg.get_rect()
        self.sRect.center = 1000, 625

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

        self.allFlakes[newFlakeID] =  {"x":random.randint(0, 1200), "y":0, "speed" : random.uniform(3,6)}

    def drawFlakes(self):
        """For each snowflake in the list, move postion and draw to screen"""
        if len(self.allFlakes) > 0:
            for key in self.allFlakes:

                self.allFlakes[key]["y"] += self.allFlakes[key]["speed"]
                self.allFlakes[key]["y"] = round(self.allFlakes[key]["y"])
                newCenterX = self.allFlakes[key]["x"]
                newCenterY = self.allFlakes[key]["y"]

                self.ffRect.center = newCenterX, newCenterY
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
        snowmanBarSurface = Panel(self.screen, 800, 180,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        snowmanSurface = Panel(self.screen, 800, 180,400,120, self.COLORS["SNOW"], alpha = 50)


        snowmanTipText1 = "SNOWMAN"
        snowmanTipText2 = (str(self.logic.snowmanCount) + " snowmen, making " + str(self.logic.snowmanFPS) + " flakes per second")
        snowmanTipText3 = ("Total flakes made by snowmen : " + str(self.logic.snowmanFlakesMade))

        if(self.mx > snowmanBarSurface.getRect()[0] and self.mx < snowmanBarSurface.getRect()[0] + snowmanBarSurface.getRect()[2] and
           self.my > snowmanBarSurface.getRect()[1] and self.my < snowmanBarSurface.getRect()[1] + snowmanBarSurface.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, snowmanSurface.getRect(), (255,255,255), self.FONTS["TEXTFONT"], snowmanTipText1, snowmanTipText2, snowmanTipText3)

        # Cookie Buy Bar & Tool Tip
        cookieBarSurface = Panel(self.screen, 800, 320,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        cookieSurface = Panel(self.screen, 800, 320,400,120, self.COLORS["SNOW"], alpha = 50)

        cookieTipText1 = "GINGERBREAD COOKIE"
        cookieTipText2 = (str(self.logic.cookieCount) + " cookies, making " + str(self.logic.cookieFPS) + " flakes per second")
        cookieTipText3 = ("Total flakes made by cookies : " + str(self.logic.cookieFlakesMade))

        if(self.mx > cookieBarSurface.getRect()[0] and self.mx < cookieBarSurface.getRect()[0] + cookieBarSurface.getRect()[2] and
           self.my > cookieBarSurface.getRect()[1] and self.my < cookieBarSurface.getRect()[1] + cookieBarSurface.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, cookieSurface.getRect(), (255,255,255), self.FONTS["TEXTFONT"], cookieTipText1, cookieTipText2, cookieTipText3)

        # Deer Buy Bar & Tool Tip
        deerBarSurface = Panel(self.screen, 800, 460,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        deerSurface = Panel(self.screen, 800, 460,400,120, self.COLORS["SNOW"], alpha = 50)

        deerTipText1 = "REINDEER"
        deerTipText2 = (str(self.logic.deerCount) + " reindeer, making " + str(self.logic.deerFPS) + " flakes per second")
        deerTipText3 = ("Total flakes made by reindeer : " + str(self.logic.deerFlakesMade))

        if(self.mx > deerBarSurface.getRect()[0] and self.mx < deerBarSurface.getRect()[0] + deerBarSurface.getRect()[2] and
           self.my > deerBarSurface.getRect()[1] and self.my < deerBarSurface.getRect()[1] + deerBarSurface.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, deerSurface.getRect(), (255,255,255), self.FONTS["TEXTFONT"], deerTipText1, deerTipText2, deerTipText3)

        # Santa Buy Bar & Tool Tip
        santaBarSurface = Panel(self.screen, 800, 600,50,120, self.COLORS["DARKGREEN"], alpha = 200)
        santaSurface = Panel(self.screen, 800, 600,400,120, self.COLORS["SNOW"], alpha = 50)

        santaTipText1 = "SANTA"
        santaTipText2 = (str(self.logic.santaCount) + " santas, making " + str(self.logic.santaFPS) + " flakes per second")
        santaTipText3 = ("Total flakes made by santas : " + str(self.logic.santaFlakesMade))

        if(self.mx > santaBarSurface.getRect()[0] and self.mx < santaBarSurface.getRect()[0] + santaBarSurface.getRect()[2] and
           self.my > santaBarSurface.getRect()[1] and self.my < santaBarSurface.getRect()[1] + santaBarSurface.getRect()[3]):
           self.toolTip.displayTip(self.screen, self.mx, self.my, -400, 0, santaSurface.getRect(), (255,255,255), self.FONTS["TEXTFONT"], santaTipText1, santaTipText2, santaTipText3)

        self.screen.blit(buySurface, (0,0))
        snowmanSurface.drawPanel()
        cookieSurface.drawPanel()
        deerSurface.drawPanel()
        santaSurface.drawPanel()

        snowmanBarSurface.drawPanel()
        cookieBarSurface.drawPanel()
        deerBarSurface.drawPanel()
        santaBarSurface.drawPanel()
        self.screen.blit(topRight, (0,0))
        self.screen.blit(self.smImg, self.smRect.center)
        self.screen.blit(self.cImg, self.cRect.center)
        self.screen.blit(self.dImg, self.dRect.center)
        self.screen.blit(self.sImg, self.sRect.center)

    """ HUD TEXT """
    def drawText(self):

        """ Snowflake Total Text """
        self.text.makeText(self.screen,'Snowflakes : ' + str(self.logic.sfCurrent), self.COLORS["TEXTCOLOR"], self.FONTS["BIGFONT"], (200, 140))

        """ Snowflake Per Second Text """
        self.text.makeText(self.screen, 'per second : ' + str(self.logic.sfps), self.COLORS["TEXTCOLOR"], self.FONTS["TEXTFONT"], (200, 170))

        """ Snowman Count """
        self.text.makeText(self.screen, str(self.logic.snowmanCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,225))

        """ Cookie Count """
        self.text.makeText(self.screen, str(self.logic.cookieCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,375))

        """ Deer Count """
        self.text.makeText(self.screen, str(self.logic.deerCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,525))

        """ Santa Count """
        self.text.makeText(self.screen, str(self.logic.santaCount), self.COLORS["TEXTCOLOR"], self.FONTS["HUGEFONT"], (1150,700))

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
                               "OPTION", pygame.Rect(560,20,90,40), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"])

        """ Info Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               "INFO", pygame.Rect(690,20,90,40), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"])

        """ Snowman Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               str(self.logic.snowmanCost), pygame.Rect(930,210,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.snowmanButtonFunc)

        """ Cookie Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               str(self.logic.cookieCost), pygame.Rect(930,350,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.cookieButtonFunc)

        """ Deer Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               str(self.logic.deerCost), pygame.Rect(930,500,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.deerButtonFunc)

        """ Santa Button """
        self.button.makeButton(self.screen, self.mx, self.my, self.mouseDown,
                               str(self.logic.santaCost), pygame.Rect(930,650,50,50), self.COLORS["MAINCOLOR"],
                               self.COLORS["HIGHLIGHTCOLOR"], self.COLORS["CLICKEDCOLOR"], self.COLORS["TEXTCOLOR"], self.FONTS["BUTTONFONT"],
                               self.santaButtonFunc)


    def snowmanButtonFunc(self):
        if self.oneClick == True:
            self.logic.snowmanBuy()
            self.oneClick = False
    def cookieButtonFunc(self):
        if self.oneClick == True:
            self.logic.cookieBuy()
            self.oneClick = False
    def deerButtonFunc(self):
        if self.oneClick == True:
            self.logic.deerBuy()
            self.oneClick = False
    def santaButtonFunc(self):
        if self.oneClick == True:
            self.logic.santaBuy()
            self.oneClick = False

    def statsToggle(self):
        if self.statsOpen == False and self.oneClick == True:
            self.statsOpen = True
            self.oneClick = False
        elif self.statsOpen == True and self.oneClick == True:
            self.statsOpen = False
            self.oneClick = False

    def statsButtonFunc(self):
        buttonFont = pygame.font.SysFont('freestyle script', 25)

        statsPanel = Panel(self.screen, 400, 80, 400, 800, self.COLORS["BLACK"], 200)
        statsPanel.drawPanel()


        self.text.makeText(self.screen, "Total snowflakes made : " + str(self.logic.sfTotal), self.COLORS["SNOW"], self.FONTS["TEXTFONT"], statsPanel.getCenter(0,-350))

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
        if self.logic.autoSpin == True:
            if self.sfSpeed < self.sfMaxSpeed:
                self.sfSpeed += self.sfAccel
            if self.sfInnerCircleSpeed < self.sfInnerCircleMaxSpeed:
                self.sfInnerCircleSpeed += self.sfInnerCircleAccel
            if self.sfOuterCircleSpeed < self.sfOuterCircleMaxSpeed:
                self.sfOuterCircleSpeed += self.sfOuterCircleAccel

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
