"""________________________________________________________________
-------------------------------------------------------------------
Program:        game.py
Author:         Tyler Jusczak
Version :       1.0
Purpose:
    Main Game program that Initiates the window and started the game loop

___________________________________________________________________
-------------------------------------------------------------------"""
import pygame
from datetime import datetime
import time
from threading import Timer
from gui import GUI
from input import Input
from logic import Logic

def main():
    "Window"
    width = 1200
    height = 800
    logic = Logic()
    gui = GUI(width, height, logic)
    input = Input(gui, logic)


    "Music"
    pygame.mixer.music.load("Music/Wish Background.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    "Loop"
    loop(width, height, gui, logic, input)

    pygame.mixer.music.stop()


def loop(width, height, gui, logic, input):

    play = True
    currentFrame = 0
    maxFrames = 60
    newSecond = None

    while(play):
        start = time.time()
        currentSecond = datetime.now()
        if currentSecond.strftime("%S") != newSecond:
            newSecond = currentSecond.strftime("%S")
            logic.update()

        events = pygame.event.get()
        input.checkQuit(events)
        input.mouseController(events)

        gui.drawBackground()
        gui.update()
        time.sleep(1/60)



main()
