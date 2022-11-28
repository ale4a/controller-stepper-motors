import components.Messages as Messages
import components.Arduino as Arduino
import time
import utils.convert as Convert
from constants.constants import MILLIMETERS
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z

class ArduinoController():
    def __init__(self, absPosition, statusDisplay):
        super().__init__()
        self.absPosition = absPosition
        self.stateAnswer = False
        self.statusDisplay  = statusDisplay
        self.lastPosition = [
            "-",
            "-",
            "-"
        ]
        self.messages = Messages.Messages()

    def setZeroPosition(self):
        self.absPosition[0] = 0
        self.absPosition[1] = 0
        self.absPosition[2] = 0
        self.statusDisplay.updateAxis()

    def getAbsolutePosition(self):
        return self.absPosition
        
    def verifyString(self, stringToVerify):
        optionsInputRead = stringToVerify.split(";")
        return len(optionsInputRead) == 4

    def verifyType(self, movement):
        return movement == "R" or movement == "A"
    
    def verifyAxis(self, axis):
        return axis == AXIS_X or axis == AXIS_Y or axis == AXIS_Z
    
    def verifyDistance(self, distance):
        return Convert.isNumber(distance)

    def convertDistance(self, distance, measure):
        distance = Convert.convertStringToNumber(distance)
        if(measure == MILLIMETERS):
            distance = Convert.convertMMToSteps(distance)
        return distance

    def getMotorMovement(self, inputRead):
        optionsInputRead = inputRead.split(";")
        typeMovement = optionsInputRead[0]
        axisMovement = optionsInputRead[1]
        stepsMovement = optionsInputRead[2]
        measure = optionsInputRead[3]
        return (axisMovement, typeMovement, stepsMovement, measure)

    def connectArduino(self, port, baudrate):
        try:
            self.arduino = Arduino.Arduino(port)
        except:
            self.messages.popupShowinfo("Error", "It is not possible to connect")
            print("it is not possible to connect")

    def closeConnection(self):
        try:
            self.arduino.isClose()
        except:
            self.messages.popupShowinfo("Error", "Do not exist variable arduino declared")
            print("Do not exist variable arduino declared")

    def addErrorForChangeOfTurn(self, distance, currentMovement, axis):
        axisNumber = 0
        if(axis == AXIS_X):
            axisNumber = 0
        if(axis == AXIS_Y):
            axisNumber = 1
        if(axis == AXIS_Z):
            axisNumber = 2
        if(currentMovement != self.lastPosition[axisNumber] and self.lastPosition[axisNumber] != '-'):
            if(currentMovement == "R"):
                distance += Convert.ERROR_WHEN_CHANGE_DIRECTION
            else:
                distance -= Convert.ERROR_WHEN_CHANGE_DIRECTION
        return distance
        
    def readOptions(self, valueInput):
        time.sleep(0.1)
        if not self.verifyString(valueInput):
            return False
        axisMovement, typeMovement, stepsMovement, measure = self.getMotorMovement(valueInput)
        if not self.verifyType(typeMovement):
            return False
        if not self.verifyAxis(axisMovement):
            return False
        if not self.verifyDistance(stepsMovement):
            return False
        distance =  self.convertDistance(stepsMovement, measure)

        if typeMovement =="R":
            time.sleep(0.1)
            if axisMovement == AXIS_X:
                self.absPosition[0] = self.absPosition[0] + distance
                currentMovement = "R" if distance > 0 else "L"
                distance = self.addErrorForChangeOfTurn(distance, currentMovement, AXIS_X)
                self.arduino.movePosition(AXIS_X, distance)
                self.lastPosition[0] = currentMovement

            elif axisMovement == AXIS_Y:
                self.absPosition[1] = self.absPosition[1] + distance
                currentMovement = "R" if distance > 0 else "L"
                distance = self.addErrorForChangeOfTurn(distance, currentMovement, AXIS_Y)
                self.arduino.movePosition(AXIS_Y, distance)
                self.lastPosition[1] = currentMovement

            elif axisMovement == AXIS_Z:
                self.absPosition[2] = self.absPosition[2] + distance
                currentMovement = "R" if distance > 0 else "L"
                distance = self.addErrorForChangeOfTurn(distance, currentMovement, AXIS_Z)
                self.arduino.movePosition(AXIS_Z, distance)
                self.lastPosition[2] = currentMovement
            self.statusDisplay.updateAxis()
            return True
        elif typeMovement =="A":
            time.sleep(0.1)
            if axisMovement == AXIS_X:
                currentMovement = "R" if distance > 0 else "L"
                steNo = distance - self.absPosition[0]
                steNo = self.addErrorForChangeOfTurn(steNo, currentMovement, AXIS_X)
                self.arduino.movePosition(AXIS_X, steNo)
                self.absPosition[0] = distance
                self.lastPosition[0] = currentMovement

            elif axisMovement == AXIS_Y:
                currentMovement = "R" if distance > 0 else "L"
                steNo = distance - self.absPosition[1]
                steNo = self.addErrorForChangeOfTurn(steNo, currentMovement, AXIS_Y)
                self.arduino.movePosition(AXIS_Y, steNo)
                self.absPosition[1] = distance
                self.lastPosition[1] = currentMovement
                
            elif axisMovement == AXIS_Z:
                currentMovement = "R" if distance > 0 else "L"
                steNo = distance - self.absPosition[2]
                steNo = self.addErrorForChangeOfTurn(steNo, currentMovement, AXIS_Z)
                self.arduino.movePosition(AXIS_Z, steNo)
                self.absPosition[2] = distance
                self.lastPosition[2] = currentMovement
            self.statusDisplay.updateAxis()
            return True

    def constantMoveController(self, axis, direction):
        self.arduino.constantMove(axis, direction)
        self.statusDisplay.updateAxis()

if __name__ == '__main__':
    pass
