#!/usr/bin/python
# -*- coding: utf-8 -*-
# move a servo from a Tk slider - scruss 2012-10-28
# read about change env
# https://code.visualstudio.com/docs/python/environments

import pyfirmata
import timing
 
board = pyfirmata.Arduino('COM4')
 
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

MIN_STEP = 10
MAX_STEP = 0
MIN_SPEED = 3500
MAX_SPEED = 2500

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def getSpeed(currentStep, totalStep):
    currentSpeed = 0
    if( currentStep <= MIN_STEP ):
        currentSpeed = _map(currentStep, 0, MIN_STEP, MIN_SPEED, MAX_SPEED)
    else:
        if (currentStep >= MAX_STEP):
            currentSpeed = _map(currentStep, MAX_STEP, totalStep, MAX_SPEED, MIN_SPEED)
        else:
            currentSpeed = MAX_SPEED
    return currentSpeed

def moveAbsoulteNumberSteps(stepsNumberToDo, stepPin, directionPin):
    if (stepsNumberToDo > 0):
        board.digital[directionPin].write(0)
    else:
        board.digital[directionPin].write(1)

    for x in range(abs(stepsNumberToDo)):
        currentStepDelay = getSpeed(x, abs(stepsNumberToDo))
        board.digital[stepPin].write(1)
        timing.delayMicroseconds(currentStepDelay)
        board.digital[stepPin].write(0)
        print(currentStepDelay)

stepPinX = 2 
dirPinX = 5

moveAbsoulteNumberSteps(200, stepPinX, dirPinX)