import components.Messages as Messages
import components.Arduino as Arduino
import serial
import time

class ArduinoController():
    def __init__(self, absPosition, statusDisplay):
        super().__init__()
        self.absPosition = absPosition
        self.stateAnswer = False
        self.statusDisplay  = statusDisplay
        self.messages = Messages.Messages()

    def getAbsoulutePosition(self):
        return self.absPosition
        
    # movimient type; axis; steps
    def verifyString(self, stringToVerify):
        optionsInputRead = stringToVerify.split(";")
        return len(optionsInputRead) == 3 

    def verifyTypeMovement(self, movement):
        return movement == "R" or movement == "A"
    
    def verifyAxisMovement(self, axis):
        return axis == "X" or axis == "Y" or axis == "Z"

    def getMotorMovement(self, inputRead):
        optionsInputRead = inputRead.split(";")
        typeMovement = optionsInputRead[0]
        axisMovement = optionsInputRead[1]
        stepsMovement = optionsInputRead[2]
        return (axisMovement, typeMovement, stepsMovement)

    def connectArduino(self, port, baudrate):
        try:
            # self.arduino = serial.Serial(port, baudrate, timeout=.1)
            self.arduino = Arduino.Arduino(port)
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
        axisMovement, typeMovement, stepsMovement = self.getMotorMovement(valueInput)
        if not self.verifyTypeMovement(typeMovement):
            return False
        if not self.verifyAxisMovement(axisMovement):
            return False
        if typeMovement =="R":
            time.sleep(0.1)
            if axisMovement == "X":
                self.absPosition[0] = self.absPosition[0] + int(stepsMovement)
                self.arduino.movePosition("X", int(stepsMovement))
            elif axisMovement == "Y":
                self.absPosition[1] = self.absPosition[1] + int(stepsMovement)
                self.arduino.movePosition("Y", int(stepsMovement))
            elif axisMovement == "Z":
                self.absPosition[2] = self.absPosition[2] + int(stepsMovement)
                self.arduino.movePosition("Z", int(stepsMovement))
            self.statusDisplay.updateAxis()
            return True
        elif typeMovement =="A":
            time.sleep(0.1)
            if axisMovement == "X":
                steNo = int(stepsMovement) - self.absPosition[0]
                self.arduino.movePosition("X", steNo)
                self.absPosition[0] = int(stepsMovement)
            elif axisMovement == "Y":
                steNo = int(stepsMovement) - self.absPosition[1]
                self.arduino.movePosition("Y", steNo)
                self.absPosition[1] = int(stepsMovement)
            elif axisMovement == "Z":
                steNo = int(stepsMovement) - self.absPosition[2]
                self.arduino.movePosition("Z", steNo)
                self.absPosition[2] = int(stepsMovement)

            self.statusDisplay.updateAxis()
            return True

if __name__ == '__main__':
    # Define the serial port and baud rate.
    # Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
    arduino = ArduinoController()
    isClose = arduino.readOptions()
    time.sleep(0.1)
