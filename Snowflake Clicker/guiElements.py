"""________________________________________________________________
-------------------------------------------------------------------
Program:        text.py
Author:         Tyler Jusczak
Version :       1.0
Purpose:
    Main Game program that Initiates the window and started the game loop

___________________________________________________________________
-------------------------------------------------------------------"""
import pygame

class Text():
    def __init__(self):
        pass

    def makeText(self, surface, text, textColor, textFont, centerPos):
        newText = textFont.render(text, True, textColor)
        newTextRect = newText.get_rect()
        newTextRect.center = centerPos
        surface.blit(newText, newTextRect)

class Button():
    def __init__(self):
        pass


    def makeButton(self,surface, mouseX, mouseY, mouseDown,
                   text, rectangle, mainColor, highlightColor,
                   clickedColor, textColor, textfont, sendFuction = None):
        buttonRect   = rectangle
        buttonRight  = buttonRect[0] + buttonRect[2]
        buttonBottom = buttonRect[1] + buttonRect[3]

        if(mouseX > buttonRect[0] and mouseX < buttonRight and
           mouseY > buttonRect[1] and mouseY < buttonBottom and mouseDown == True):
            pygame.draw.rect(surface, clickedColor, buttonRect)
            if(sendFuction != None):
                sendFuction()

        elif(mouseX > buttonRect[0] and mouseX < buttonRight and
             mouseY > buttonRect[1] and mouseY < buttonBottom and mouseDown != True):
            pygame.draw.rect(surface, highlightColor, buttonRect)

        else:
            pygame.draw.rect(surface, mainColor, buttonRect)

        buttonText            = textfont.render(text, True, textColor)
        buttonTextRect        = buttonText.get_rect()
        buttonTextRect.center = (buttonRect[0] + (buttonRect[2]/2) ,buttonRect[1] + (buttonRect[3]/2))
        surface.blit(buttonText, buttonTextRect)

class Panel():
    def __init__(self, surface, left, top, height, width, color, alpha = 255):
        w, h = surface.get_size()
        self.surface = surface
        self.panelSurface = pygame.Surface((w, h))
        self.panelSurfaceRect = pygame.Rect(left,top,height,width)
        self.panelSurface.set_colorkey((0,0,0))
        self.panelSurface.set_alpha(alpha)
        pygame.draw.rect(self.panelSurface, color,self.panelSurfaceRect)
    def drawPanel(self):

        self.surface.blit(self.panelSurface, (0,0))

    def getRect(self):
        return self.panelSurfaceRect

    def getCenter(self, xOffset = 0, yOffset = 0):
        center = (self.panelSurfaceRect[0] + (self.panelSurfaceRect[2]/2) + xOffset,
                  self.panelSurfaceRect[1] + (self.panelSurfaceRect[3]/2) +yOffset)
        return center

class ToolTip():
    def __init__(self):
        pass


    def displayTip(self,surface, mouseX, mouseY, xOffset, yOffset,
                   rectangle, textColor, textfont,
                   textLineOne = "", textLineTwo = "", textLineThree =""):

        tipRect   = rectangle
        tipRight  = tipRect[0] + tipRect[2]
        tipBottom = tipRect[1] + tipRect[3]

        if(mouseX > tipRect[0] and mouseX < tipRight and
           mouseY > tipRect[1] and mouseY < tipBottom):
            tipSurface = pygame.Surface((1200,800))
            tipRect = pygame.Rect(tipRect[0] + xOffset,tipRect[1],tipRect[2] + yOffset,tipRect[3])
            tipSurface.set_colorkey((0,0,0))
            tipSurface.set_alpha(200)
            pygame.draw.rect(tipSurface, (25,25,25),tipRect)


            lineOne = textfont.render(textLineOne, True, textColor)
            lineOneRect = lineOne.get_rect()
            lineOneRect.center = (tipRect[0] + (tipRect[2]/2),
                                  tipRect[1] - 40 + (tipRect[3]/2))

            lineTwo = textfont.render(textLineTwo, True, textColor)
            lineTwoRect = lineTwo.get_rect()
            lineTwoRect.center = (tipRect[0] + (tipRect[2]/2),
                                  tipRect[1] + (tipRect[3]/2))

            lineThree = textfont.render(textLineThree, True, textColor)
            lineThreeRect = lineThree.get_rect()
            lineThreeRect.center = (tipRect[0] + (tipRect[2]/2),
                                    tipRect[1] + 40 + (tipRect[3]/2))

            surface.blit(tipSurface, (0,0))
            surface.blit(lineOne, lineOneRect)
            surface.blit(lineTwo, lineTwoRect)
            surface.blit(lineThree, lineThreeRect)

class CircleGrowAnim():
    def __init__(self,surface, width, height, color, alpha, radius):

        self.ORGRADIUS = radius

        self.surface = surface
        self.w = width
        self.h = height
        self.alpha = alpha
        self.color = color
        self.radius = radius

        self.maxGrow = 1.24
        self.upSpeed = 0.12
        self.DOWNSPEED = 0.009
        self.downSpeed = self.DOWNSPEED
        self.downAccel = 0.001


        self.grow = False

    def clicked(self):
        if self.radius < self.ORGRADIUS * self.maxGrow:
            self.downSpeed = self.DOWNSPEED
            self.grow = True

    def update(self):
        if self.grow == True:
            self.radius += self.radius * self.upSpeed
            self.grow = False

        if self.radius >= self.ORGRADIUS * self.maxGrow:
            self.grow = False
            self.radius = self.ORGRADIUS * self.maxGrow

        if self.grow == False:
            self.radius -= self.radius * self.downSpeed
            self.downSpeed += self.downAccel

        if self.radius <= self.ORGRADIUS:
            self.radius = self.ORGRADIUS
            self.downSpeed = self.DOWNSPEED

        animLayer = pygame.Surface((1200, 800))
        animLayer.set_alpha(self.alpha)
        animLayer.set_colorkey((0,0,0))
        pygame.draw.circle(animLayer, self.color, (self.w, self.h), self.radius)
        self.surface.blit(animLayer, (0,0))
