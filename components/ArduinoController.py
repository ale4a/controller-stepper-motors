import serial
import time
import serialPorts

class ArduinoController():
    def __init__(self):
        super().__init__()
        a = serialPorts.connect()
        
    def connectArduino(self, port, baudrate):
        self.arduino = serial.Serial(port, baudrate, timeout=.1)

    def readOptions(self, inputRead):
        self.readOptions(inputRead)
        time.sleep(0.1)

    # movimient type; axis;  steps
    def verifyString(self, stringToVerify):
        optionsInputRead = stringToVerify.split(";")
        return len(optionsInputRead) == 3

    def getMotorMovement(self, inputRead):
        optionsInputRead = inputRead.split(";")
        typeMovement = optionsInputRead[0]
        axisMovement = optionsInputRead[1]
        stepsMovement = optionsInputRead[2]
        return (axisMovement, typeMovement, stepsMovement)

    def closeConnection(self):
        time.sleep(0.1)
        self.arduino.close()

    def readOptions(self, valueInput):
        if self.verifyString(valueInput):
            axisMovement, typeMovement, stepsMovement = self.getMotorMovement(valueInput)
            command =  typeMovement+ axisMovement + stepsMovement + "\n"
            print('typeMovement', stepsMovement)
            if typeMovement =="R":
                time.sleep(0.1) 
                self.arduino.write(bytes(command, 'utf-8'))
            elif typeMovement =="A":
                time.sleep(0.1)
                self.arduino.write(bytes(command, 'utf-8'))
            else:
                print("Invalid input. Type on / off / quit.")
        else:
            print("Invalid input. Type on / off / quit.")
    
if __name__ == '__main__':
    # Define the serial port and baud rate.
    # Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
    arduino = ArduinoController()
    isClose = arduino.readOptions()
    time.sleep(0.1)
