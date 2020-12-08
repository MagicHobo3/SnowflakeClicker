"""________________________________________________________________
-------------------------------------------------------------------
Program:        input.py
Author:         Tyler Jusczak
Version :       1.0
Purpose:
___________________________________________________________________
-------------------------------------------------------------------"""
import pygame
import random

class Input(object):

    def __init__(self, gui, logic):
        pygame.init()

        self.gui = gui
        self.logic = logic

    def mouseController(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                MX, MY = pygame.mouse.get_pos()
                self.gui.mx = MX
                self.gui.my = MY

            if event.type == pygame.MOUSEBUTTONDOWN:
                MX, MY = pygame.mouse.get_pos()
                self.gui.mouseDown = True

                # Mouse Clicked on Snowflake
                sfRect = self.gui.sfRect
                if MX > sfRect.left and MX < sfRect.right and MY > sfRect.top and MY < sfRect.bottom:
                    if self.gui.sfSpeed < self.gui.sfMaxSpeed:
                        self.gui.sfSpeed += self.gui.sfAccel
                    if self.gui.sfOuterCircleSpeed < self.gui.sfOuterCircleMaxSpeed:
                        self.gui.sfOuterCircleSpeed += self.gui.sfOuterCircleAccel
                    if self.gui.sfInnerCircleSpeed < self.gui.sfInnerCircleMaxSpeed:
                        self.gui.sfInnerCircleSpeed += self.gui.sfInnerCircleAccel
                    self.gui.newFlake()
                    for back in self.gui.snowBackCircle:
                        back.clicked()
                    self.logic.snowButtonClicked()


            if event.type == pygame.MOUSEBUTTONUP:
                MX, MY = pygame.mouse.get_pos()
                self.gui.mouseDown = False
                self.gui.oneClick = True


    def checkQuit(self, events):

        for event in events:

            if(event.type == pygame.QUIT):
                running = False
                pygame.quit()
                quit()

    def sfClick(self, events):
        MX, MY = mouceClickPOS()
        print(MX)
        print(MY)



    def update(self, controller):
        pass
