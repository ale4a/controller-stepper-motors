"""
steps  - mm
80      1 mm 
160     2 mm 
"""

MM = 1
STEPS = 90

def convertStepsToMM(steps):
    return round((steps * MM) / STEPS, 2)

def convertMMToSteps(mm):
    return int((mm * STEPS) / MM )

def isFloatNumber(NumberString):
    NumberString = NumberString.replace('-','',1)
    return NumberString.replace('.','',1).isdigit() and NumberString.count('.') < 2

def isIntNumber(NumberString):
    NumberString = NumberString.replace('-','',1)
    return NumberString.isdigit()

# Function verify if is int or float number
def isNumber(number):
    return isIntNumber(number) or isFloatNumber(number)

# Function that permits convert String into number
def convertStringToNumber(number):
    if(isIntNumber(number)):
        return int(number)
    if(isFloatNumber(number)):
        return float(number)
