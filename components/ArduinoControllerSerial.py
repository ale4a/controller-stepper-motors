import components.Messages as Messages
import serial
import time
import utils.convert as Convert
from constants.constants import MILLIMETERS
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z

class ArduinoControllerSerial():
    """
        This code create a connection between python and arduino using Serial library
    """
    def __init__(self, absPosition, statusDisplay):
        super().__init__()
        self.absPosition = absPosition
        self.stateAnswer = False
        self.statusDisplay  = statusDisplay
        self.messages = Messages.Messages()

    def setZeroPosition(self):
        """
            set zero position and update axis display
        """
        self.absPosition[0] = 0
        self.absPosition[1] = 0
        self.absPosition[2] = 0
        self.statusDisplay.updateAxis()

    def getAbsolutePosition(self):
        """
            Return
                absPosition
        """
        return self.absPosition
        
    def verifyString(self, stringToVerify):
        """
            Verify if the string has 4 position 

            Parameters
                stringToVerify
        """
        optionsInputRead = stringToVerify.split(";")
        return len(optionsInputRead) == 4 

    def verifyType(self, movement):
        """
            Verify type of movement Relative or Absolute
        """
        return movement == "R" or movement == "A"
    
    def verifyAxis(self, axis):
        return axis == AXIS_X or axis == AXIS_Y or axis == AXIS_Z

    def verifyDistance(self, distance):
        return Convert.isNumber(distance)

    def convertDistance(self, distance, measure):
        """
            This function convert the distance in millimeters
        """
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

    def connectArduino(self, port, baudrate = 9600):
        """
            Connect with the class arduino
        """
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=.1)
        except:
            self.messages.popupShowinfo("Error", "It is not possible to connect")
            print("it is not possible to connect")

    def closeConnection(self):
        """
            Close the connection with arduino
        """
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
        """
            Function that read string with the commands necessary to move, 
            
            Evaluate 
                - verify value input is a correct command
                - relative or absolute movement
                - if it is necessary to add steps to make up for the mistake
                - save absolute position

            Parameters:
                valueInput: commands that you should move
        """
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

    def constantsMoveController(self, axis, direction):
        """
            This function could not be done using serial connection
        """
        pass

if __name__ == '__main__':
    pass
