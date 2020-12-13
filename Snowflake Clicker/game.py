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
import os
import pickle
from gui import GUI
from input import Input
from logic import Logic

def main():
    "Window"
    width = 1200
    height = 800


    # This is what I orinally had. But I needed to use Try/Except somewhere.
    """
    if os.path.exists("savedata.txt"):
        load = open('savedata.txt', 'rb')
        logic = pickle.load(load)
        load.close()
        print("Loaded Saved Game")
    else:
        logic = Logic()
        print("New Game")
    """

    # If saved data exists, load that data as the Logic Class
    try:
        load = open('savedata.txt', 'rb')
        logic = pickle.load(load)
        load.close()
        print("Loaded Saved Game : " + str(logic.lastSave))
    # Else pull in a fresh Logic Class
    except:
        logic = Logic()
        print("New Game")

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
    newMinute = None

    while(play):
        currentTime = datetime.now()
        if currentTime.strftime("%S") != newSecond:
            newSecond = currentTime.strftime("%S")
            logic.update()
        if currentTime.strftime("%M") != newMinute:
            newMinute = currentTime.strftime("%M")
            gui.pickle()

        events = pygame.event.get()
        input.checkQuit(events)
        input.mouseController(events)

        gui.drawBackground()
        gui.update()
        time.sleep(1/60)



main()
