import serial
import time
import serialPorts

class ArduinoController():
    def __init__(self, absPosition):
        super().__init__()
        serialPorts.connect()
        self.absPosition = absPosition
        self.stateAnswer = False
        print(self.absPosition)

    # movimient type; axis; steps
    def verifyString(self, stringToVerify):
        optionsInputRead = stringToVerify.split(";")
        return len(optionsInputRead) == 3

    def getMotorMovement(self, inputRead):
        optionsInputRead = inputRead.split(";")
        typeMovement = optionsInputRead[0]
        axisMovement = optionsInputRead[1]
        stepsMovement = optionsInputRead[2]
        return (axisMovement, typeMovement, stepsMovement)

    def connectArduino(self, port, baudrate):
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=.1)
        except:
            print("it is not possible to connect")

    def closeConnection(self):
        try:
            if self.arduino.isOpen() == True:
                self.arduino.close()
            else:
                print("it is not open")
        except:
            print("Do not exist variable arduino declared")

    def readOptions(self, valueInput):
        time.sleep(0.1)
        if self.verifyString(valueInput):
            axisMovement, typeMovement, stepsMovement = self.getMotorMovement(valueInput)
            command =  typeMovement + axisMovement + stepsMovement + "\n"
            print('typeMovement', stepsMovement)
            if typeMovement =="R":
                time.sleep(0.1)
                self.arduino.write(bytes(command, 'utf-8'))
                if axisMovement == "X":
                    self.absPosition[0] = self.absPosition[0] + int(stepsMovement)
                elif axisMovement == "Y":
                    self.absPosition[1] = self.absPosition[1] + int(stepsMovement)
                elif axisMovement == "Z":
                    self.absPosition[2] = self.absPosition[2] + int(stepsMovement)
                return True
            elif typeMovement =="A":
                time.sleep(0.1)
                self.arduino.write(bytes(command, 'utf-8'))
                if axisMovement == "X":
                    self.absPosition[0] = int(stepsMovement)
                    print(self.absPosition)
                elif axisMovement == "Y":
                    self.absPosition[1] = int(stepsMovement)
                    print(self.absPosition)
                elif axisMovement == "Z":
                    self.absPosition[2] = int(stepsMovement)
                    print(self.absPosition)
                return True
            else:
                print("Invalid input.")
                return False
        else:
            print("Invalid input")
            return False

if __name__ == '__main__':
    # Define the serial port and baud rate.
    # Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
    arduino = ArduinoController()
    isClose = arduino.readOptions()
    time.sleep(0.1)
