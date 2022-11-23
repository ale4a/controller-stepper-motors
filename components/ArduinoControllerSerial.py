import components.Messages as Messages
import serial
import time
import utils.convert as Convert
from constants.constants import MILLIMITERS
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z

class ArduinoControllerSerial():
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
        return axis == AXIS_X or axis == AXIS_Y or axis == AXIS_Z

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

    def connectArduino(self, port, baudrate = 9600):
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=.1)
        except:
            self.messages.popupShowinfo("Error", "It is not possible to connect")
            print("it is not possible to connect")

    def closeConnection(self):
        try:
            if self.arduino.isOpen() == True:
                self.arduino.close()
            else:
                self.messages.popupShowinfo("Error", "It is not open")
                print("it is not open")
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
        command =  typeMovement + axisMovement + str(distance) + "\n"
        if typeMovement =="R":
            time.sleep(0.1)
            self.arduino.write(bytes(command, 'utf-8'))
            if axisMovement == AXIS_X:
                self.absPosition[0] = self.absPosition[0] + distance
            elif axisMovement == AXIS_Y:
                self.absPosition[1] = self.absPosition[1] + distance
            elif axisMovement == AXIS_Z:
                self.absPosition[2] = self.absPosition[2] + distance
            self.statusDisplay.updateAxis()
            return True
        elif typeMovement =="A":
            time.sleep(0.1)
            self.arduino.write(bytes(command, 'utf-8'))
            if axisMovement == AXIS_X:
                steNo = distance - self.absPosition[0]
                command =  typeMovement + axisMovement + str(steNo) + "\n"
                self.arduino.write(bytes(command, 'utf-8'))
                self.absPosition[0] = distance
            elif axisMovement == AXIS_Y:
                steNo = distance - self.absPosition[1]
                command =  typeMovement + axisMovement + str(steNo) + "\n"
                self.arduino.write(bytes(command, 'utf-8'))
                self.absPosition[1] = distance
            elif axisMovement == AXIS_Z:
                steNo = distance - self.absPosition[2]
                command =  typeMovement + axisMovement + str(steNo) + "\n"
                self.arduino.write(bytes(command, 'utf-8'))
                self.absPosition[2] = distance
            self.statusDisplay.updateAxis()
            return True

    def constansMoveController(self, axis, direction):
        # self.arduino.constansMove(axis, direction)
        # self.statusDisplay.updateAxis()
        pass

if __name__ == '__main__':
    # Define the serial port and baud rate.
    # Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
    arduino = ArduinoControllerSerial()
    isClose = arduino.readOptions()
    time.sleep(0.1)
