from asyncio.windows_events import NULL
import pyfirmata
import time
import re

#defines pins numbers
stepPinX = 2
dirPinX = 5
stepPinY= 3
dirPinY = 6
stepPinZ = 4
dirPinZ = 7

currentFrequency = 0 # frequency in Hz (max value 1600 Hz for half step mode)
firstStepDelay = 0   # delay for stepper pulse duration
secondStepDelay = 0  # delay for stepper pulse duration

positionToMove = 0 
steps = 0           
stepNo = 0           # steps to do
#current position
absPositionx = 0
absPositiony = 0
absPositionz = 0


inCommandByte = ''  # 1st incoming serial byte
inAxisByte = ''     # 2nd incomming byte
inData = 0
inByteCount = 0     # received bytes
serBuffer = []
inDataStr = ""


currentFrequency = 2000000
#myStepDelay=1000000 / currentFrequency/2;
firstStepDelay = 400000 / currentFrequency
secondStepDelay = 600000 / currentFrequency
# Initiate communication with Arduino

board = pyfirmata.Arduino('COM4')    
print("Communication Successfully started")

def separateNumberChars(stringToVerify):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', stringToVerify.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return res_f

def verifyString(stringToVerify):
    return len(stringToVerify) == 2

def getMotorMovement(inputRead):
    inputSeparate = separateNumberChars(inputRead)
    if verifyString(inputSeparate):
        axisAndTypeMovement = inputSeparate[0]
        axisMovement = axisAndTypeMovement[1]
        typeMovement = axisAndTypeMovement[0]
        timeMovement = inputSeparate[1]
        return [axisMovement, typeMovement, timeMovement]
    else:
        return NULL


def moveAbsoulteNumberSteps(stepsNumberToDo, stepPin, directionPin):    
    motorDirection = 0
    if (stepsNumberToDo > 0):
        # clockwise direction
        board.digital[directionPin].write(1)
        motorDirection = 1
    else:
        # anticlockwise direction
        board.digital[directionPin].write(0)
        motorDirection = -1
    print("stepsNumberToDo", stepsNumberToDo)
    for x in range(abs(stepsNumberToDo)):
        board.digital[stepPin].write(1)
        time.sleep(firstStepDelay)
        board.digital[stepPin].write(0)
        time.sleep(firstStepDelay)
        # time.sleep(0000000000000.1)
    
    stepCounter = abs(stepsNumberToDo) * motorDirection
    return stepCounter


if __name__ == '__main__':
    while True:
        print("------- Options ------------")
        print("1. Relative eg: RX100 RY100")
        print("2. Absolute eg: AX100 AY100")
        print("----------------------------")

        valueInput = input("Enter your data ... ")
        motorAxis, motorTypeMovement, stepNo = getMotorMovement(valueInput)
        stepNo = int(stepNo)
        print(motorAxis)
        print(motorTypeMovement)
        print(stepNo)

        if motorTypeMovement == "R":
            if motorAxis == "X":
                steps = moveAbsoulteNumberSteps(stepNo, stepPinX, dirPinX)
                print("----------- X -----------")
            elif motorAxis == "Y":
                steps = moveAbsoulteNumberSteps(stepNo, stepPinY, dirPinY)
                print("----------- Y -----------")
            elif motorAxis == "Z":
                steps = moveAbsoulteNumberSteps(stepNo, stepPinZ, dirPinZ)
                print("----------- Z -----------")
        else:
            print("No axis detected!")