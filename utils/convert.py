"""
This data has been obtained thanks a calculate steps to mm for later build a Linear Regression    
    Review 
    tableData.excel
"""
positiveSlope = 90.476
positiveConstant = -0.4195

"""ERROR_WHEN_CHANGE_DIRECTION
    This error is necessary to add when change the direction of motor
"""
ERROR_WHEN_CHANGE_DIRECTION = 18

"""ConvertStepsToMM
    Transform steps to mm with round 2 decimals using inverse function of Linear Regression

    Parameters
        steps: millimeters that you want to convert
    Returns
        number with 2 decimal
"""
def convertStepsToMM(steps):
    res = (steps - positiveConstant) / positiveSlope
    return round(res, 2)

"""ConvertMMToSteps
    Transform millimeters to steps in integer number using Linear Regression

    Parameters
        millimeters: number
    Returns
        Integer number
"""
def convertMMToSteps(millimeters):
    res = positiveSlope * millimeters + positiveConstant
    return int(round(res))

"""isFloatNumber
    Verify if a string can be a float number 
    Parameters
        numberString: string 
    Returns
        True or False
"""
def isFloatNumber(numberString):
    numberString = numberString.replace('-','',1)
    return numberString.replace('.','',1).isdigit() and numberString.count('.') < 2

"""isIntNumber
    Verify if a string can be a int number 
    Parameters
        numberString: string 
    Returns
        True or False
"""
def isIntNumber(numberString):
    numberString = numberString.replace('-','',1)
    return numberString.isdigit()

"""isNumber
    Verify if a string can be a int number or float number 
    Parameters
        number: string
    Returns
        True or False
"""
def isNumber(number):
    return isIntNumber(number) or isFloatNumber(number)

"""convertStringToNumber
    convert string number in int or float number
    Parameters
        number: string
    Returns
        float or int number

"""
def convertStringToNumber(number):
    if(isIntNumber(number)):
        return int(number)
    if(isFloatNumber(number)):
        return float(number)
    return number
