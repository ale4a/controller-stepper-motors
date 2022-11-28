import pyfirmata
import components.timing as timing
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z

MIN_STEP = 0
MAX_STEP = 0
# this means that 5% started fast and 90% MAX_SPEED and 5% finish slow
percentageToPerform = 35
MIN_SPEED = 7000
MAX_SPEED = 5000

class Arduino():
    """
        This class create connection between python and arduino using pyfirmata
    """
    def __init__(self, port):
        """
            Parameters
            port: the string that has reference to the port
        """
        self.port = port
        self.board = pyfirmata.Arduino(port)
        self.iter8 = pyfirmata.util.Iterator(self.board)
        self.iter8.start()
        self.stepPinX = 2 
        self.dirPinX = 5
        self.stepPinX = 2
        self.dirPinX = 5
        self.stepPinY= 3
        self.dirPinY = 6
        self.stepPinZ = 4
        self.dirPinZ = 7
   

    def _map(self, value, fromLow, fromHigh, toLow, toHigh):
        """
            That is, a value of fromLow would get mapped to toLow, a value of fromHigh to toHigh, values in-between to values in-between, etc.

            Parameters
            value: the number to map.
            fromLow: the lower bound of the value’s current range.
            fromHigh: the upper bound of the value’s current range.
            toLow: the lower bound of the value’s target range.
            toHigh: the upper bound of the value’s target range.

            Returns
            The mapped value. Data type: long.
        """
        return int((value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow)

    def calculateProportion(self, value, percentage):
        """
            Calculate de percentage of speed give it a number
        """
        return value * (percentage/100)

    def getSpeed(self, currentStep, totalStep):
        currentSpeed = 0
        MIN_STEP = self.calculateProportion(totalStep, percentageToPerform)
        if(totalStep < 700):
            return MIN_SPEED
        if( currentStep <= MIN_STEP ):
            currentSpeed = self._map(currentStep, 0, MIN_STEP, MIN_SPEED, MAX_SPEED)
            return currentSpeed

        MAX_STEP = totalStep - MIN_STEP
        if (currentStep >= MAX_STEP):
            currentSpeed = self._map(currentStep, MAX_STEP,totalStep , MAX_SPEED, MIN_SPEED)
            return currentSpeed
        return MAX_SPEED

    def moveNumberSteps(self, stepsNumberToDo, stepPin, directionPin):
        if (stepsNumberToDo > 0):
            self.board.digital[directionPin].write(0)
        else:
            self.board.digital[directionPin].write(1)
        for x in range(abs(stepsNumberToDo)):
            currentStepDelay = self.getSpeed(x, abs(stepsNumberToDo))
            self.board.digital[stepPin].write(1)
            timing.delayMicroseconds(currentStepDelay)
            self.board.digital[stepPin].write(0)
            timing.delayMicroseconds(currentStepDelay)

    def movePosition(self, axis, steps):
        if(axis == AXIS_X):
            self.moveNumberSteps(steps, self.stepPinX, self.dirPinX)
        if(axis == AXIS_Y):
            self.moveNumberSteps(steps, self.stepPinY, self.dirPinY)
        if(axis == AXIS_Z):
            self.moveNumberSteps(steps, self.stepPinZ, self.dirPinZ)
    
    def getAxis(self, axis):
        if(axis == AXIS_X):
            return (self.dirPinX, self.stepPinX)
        if(axis == AXIS_Y):
            return (self.dirPinY, self.stepPinY)
        if(axis == AXIS_Z):
            return (self.dirPinZ, self.stepPinZ)

    def constantMove(self, axis, direction):
        directionPin, stepPin = self.getAxis(axis)
        if (direction > 0):
            self.board.digital[directionPin].write(0)
        else:
            self.board.digital[directionPin].write(1)

        currentStepDelay = 1400
        for x in range(abs(4)):
            self.board.digital[stepPin].write(1)
            timing.delayMicroseconds(currentStepDelay)
            self.board.digital[stepPin].write(0)

    def isClose(self):
        self.board.exit()

if __name__ == '__main__':
    arduino = Arduino("COM4")
    arduino.movePosition(AXIS_X, 200)
    arduino.movePosition(AXIS_Y, 200)
