"""
steps  - mm
80      1 mm 
160     2 mm 
"""

MM = 1
STEPS = 80
def convertStepsToMM(steps):
    return int((steps * MM) / STEPS )

def convertMMToSteps(mm):
    return int((mm * STEPS) / MM )