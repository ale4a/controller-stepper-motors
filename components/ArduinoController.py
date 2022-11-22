import components.Messages as Messages
import components.Arduino as Arduino
import time

import utils.convert as Convert
from constants.constants import MILLIMITERS
class ArduinoController():
    def __init__(self, absPosition, statusDisplay):
        super().__init__()
        self.absPosition = absPosition
        self.stateAnswer = False
        self.statusDisplay  = statusDisplay
        self.messages = Messages.Messages()

    def setZeroPosition(self):
        self.absPosition[0] = 0
        self.absPosition[1] = 0
        self.absPosition[2] = 0
        self.statusDisplay.updateAxis()

    def getAbsoulutePosition(self):
        return self.absPosition
        
    def verifyString(self, stringToVerify):
        optionsInputRead = stringToVerify.split(";")
        return len(optionsInputRead) == 4

    def verifyType(self, movement):
        return movement == "R" or movement == "A"
    
    def verifyAxis(self, axis):
        return axis == "X" or axis == "Y" or axis == "Z"
    
    def verifyDistance(self, distance):
        return Convert.isNumber(distance)

    def convertDistance(self, distance, measure):
        distance = Convert.convertStringToNumber(distance)
        if(measure == MILLIMITERS):
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
            if axisMovement == "X":
                self.absPosition[0] = self.absPosition[0] + distance
                self.arduino.movePosition("X", distance)
            elif axisMovement == "Y":
                self.absPosition[1] = self.absPosition[1] + distance
                self.arduino.movePosition("Y", distance)
            elif axisMovement == "Z":
                self.absPosition[2] = self.absPosition[2] + distance
                self.arduino.movePosition("Z", distance)
            self.statusDisplay.updateAxis()
            return True
        elif typeMovement =="A":
            time.sleep(0.1)
            if axisMovement == "X":
                steNo = distance - self.absPosition[0]
                self.arduino.movePosition("X", steNo)
                self.absPosition[0] = distance
            elif axisMovement == "Y":
                steNo = distance - self.absPosition[1]
                self.arduino.movePosition("Y", steNo)
                self.absPosition[1] = distance
            elif axisMovement == "Z":
                steNo = distance - self.absPosition[2]
                self.arduino.movePosition("Z", steNo)
                self.absPosition[2] = distance

            self.statusDisplay.updateAxis()
            return True

    def constansMoveController(self, axis, direction):
        self.arduino.constansMove(axis, direction)
        self.statusDisplay.updateAxis()


if __name__ == '__main__':
    # Define the serial port and baud rate.
    # Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
    #arduino = ArduinoController()
    #isClose = arduino.readOptions()
    #time.sleep(0.1)
    pass
