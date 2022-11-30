import pyfirmata
import components.timing as timing
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z

MIN_STEP = 0
MAX_STEP = 0
# this means that [35]% started fast and 30% MAX_SPEED and 35% finish slow
percentageToPerform = 35
# The higher the number, the slower speed
MIN_SPEED = 7000
# The smaller the number, the faster speed
MAX_SPEED = 5000
# Any movement below of this step will be MIN_SPEED
MAX_SPEED_TOTAL = 700

class Arduino():
    """
        This class create connection between python and arduino using pyfirmata
    """
    def __init__(self, port):
        """
            Constructor to define port and pins that are being used in arduino

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

            Return
                The mapped value. Data type: long.
        """
        return int((value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow)

    def calculateProportion(self, value, percentage):
        """
            Create a proportion speed ramp, the ramp will grow to this proportion until point A and it will start to decrease from the same speed from point B
                 A           B 
                 |           |
                 _____________
                /             \
               /               \  
              /                 \
            _/                   \_

            Return
                The number of proportion to create speed ramp
        """
        return value * (percentage/100)

    def getSpeed(self, currentStep, totalStep):
        """
            This function get the speed required, when total speed is less than MAX_SPEED_TOTAL this function returns a MIN_SPEED
            because accuracy is being given more priority than speed.

            But in other case is greater than MAX_SPEED_TOTAL this function calculate a speed in the form of a ramp once the operation if
            the engine begins and ends

            Parameters
                currentStep: it is the current step where is motor
                totalStep: the total of steps that is necessary to move
            Return
                currentSpeed: speed at a certain pint
        """
        currentSpeed = 0
        MIN_STEP = self.calculateProportion(totalStep, percentageToPerform)
        if(totalStep < MAX_SPEED_TOTAL):
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
        """
            This function will move the amount of steps number to do in a certain direction

            Parameters
                stepsNumberToDo: number of steps what is going to move
                stepPin: step pin which uses the given axis
                directionPin: direction pint which uses the given axis
        """
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
        """
            Function calls to moveNumberSteps to determine on which axis and how much it will move
            Parameters
                axis: axis where the action will be executed
                steps:  steps that you move in a determine axi
        """
        if(axis == AXIS_X):
            self.moveNumberSteps(steps, self.stepPinX, self.dirPinX)
        if(axis == AXIS_Y):
            self.moveNumberSteps(steps, self.stepPinY, self.dirPinY)
        if(axis == AXIS_Z):
            self.moveNumberSteps(steps, self.stepPinZ, self.dirPinZ)
    
    def getAxis(self, axis):
        """
            Get dir and step pin of a certain axis
            Parameters
                axis: axis where the action will be executed
            Return
                dirPin, stepPin
        """
        if(axis == AXIS_X):
            return (self.dirPinX, self.stepPinX)
        if(axis == AXIS_Y):
            return (self.dirPinY, self.stepPinY)
        if(axis == AXIS_Z):
            return (self.dirPinZ, self.stepPinZ)

    def constantMove(self, axis, direction):
        """
            This function helps you to have a constant movement once required

            Parameters
                axis: axis where the action will be executed
                direction: positive or negative direction

        """
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
        """
            Close the connection between python and arduino
        """
        self.board.exit()

if __name__ == '__main__':
    pass
