# arduino_LED_user.py

import serial
import time

# movimient type; axis;  steps
def verifyString(stringToVerify):
    optionsInputRead = stringToVerify.split(";")
    return len(optionsInputRead) == 3

def getMotorMovement(inputRead):
    optionsInputRead = inputRead.split(";")
    typeMovement = optionsInputRead[0]
    axisMovement = optionsInputRead[1]
    stepsMovement = optionsInputRead[2]
    return (axisMovement, typeMovement, stepsMovement)


def readOptions():
    print("----------------------- Options ----------------------------")
    print("1. Relative position, e.g. R;X;100 [Relative, Axis, steps]")
    print("2. Absolute position, e.g. A;X;100 [Absolute, Axis, steps]")
    print("3. Quit")
    print("------------------------------------------------------------")
    valueInput = input("Enter your data ... ")

    if valueInput =="quit" or valueInput == "q":
        print("Program Exiting")
        time.sleep(0.1)
        ser.close()
        return True
    elif verifyString(valueInput):
        axisMovement, typeMovement, stepsMovement = getMotorMovement(valueInput)
        command =  typeMovement+ axisMovement + stepsMovement + "\n"
        print('typeMovement', stepsMovement)
        if typeMovement =="R":
            time.sleep(0.1) 
            ser.write(bytes(command, 'utf-8'))
        elif typeMovement =="A":
            time.sleep(0.1)
            ser.write(bytes(command, 'utf-8'))
        else:
            print("Invalid input. Type on / off / quit.")
    else:
        print("Invalid input. Type on / off / quit.")
    
if __name__ == '__main__':
    # Define the serial port and baud rate.
    # Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
    ser = serial.Serial('COM4', 9600)
    time.sleep(2) # wait for the serial connection to initialize

    while True:   
        isClose = readOptions()
        time.sleep(0.1)
        if isClose:
            break


