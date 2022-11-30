# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT
from tkinter import Tk, Label
from tkinter import Frame
import utils.convert as Convert

class CoordinateState(Frame):
    """
        This class draw coordinate state
    """
    def __init__(self, parent, absPosition):
        super().__init__()
        self.parent = parent
        self.absPosition = absPosition
        self.createWidgets()

    def getValueStepsString(self, steps):
        mm = Convert.convertStepsToMM(int(steps))
        return "{} steps / {} mm".format(steps,mm)

    def updateAxis(self):
        self.axisXValue.config(text = self.getValueStepsString(str(self.absPosition[0])))
        self.axisYValue.config(text = self.getValueStepsString(str(self.absPosition[1])))
        self.axisZValue.config(text = self.getValueStepsString(str(self.absPosition[2])))

    def createWidgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {"pady": 2, "padx":5}
        stylesLabel = {
            # "bg": "white", 
            "width": 18
        }
        # - - - - - - - - - - - - - - - - - - - - -
        # Axis X
        self.axisXLabel = Label(self.parent, text="X:", font=fontState)
        self.axisXLabel.grid(row = 0, column = 0, **padding)
        self.axisXValue = Label(self.parent, text = self.getValueStepsString(str(self.absPosition[0])), font=fontState, **stylesLabel)
        self.axisXValue.grid(row = 0, column = 1, **padding)
        # - - - - - - - - - - - - - - - - - - - - -
        # Axis Y
        self.axisYLabel = Label(self.parent, text="Y:", font=fontState)
        self.axisYLabel.grid(row = 1, column = 0,  **padding)
        self.axisYValue = Label(self.parent, text = self.getValueStepsString(str(self.absPosition[1])), font=fontState, **stylesLabel)
        self.axisYValue.grid(row = 1, column = 1, **padding)
        # - - - - - - - - - - - - - - - - - - - - -
        # Axis Z
        self.axisZLabel = Label(self.parent, text="Z:", font=fontState)
        self.axisZLabel.grid(row = 2, column = 0, **padding)
        self.axisZValue = Label(self.parent, text = self.getValueStepsString(str(self.absPosition[2])), font=fontState, **stylesLabel)
        self.axisZValue.grid(row = 2, column = 1, **padding)
        # - - - - - - - - - - - - - - - - - - - - -

class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x500")
        self.parent.title('Software to scanner')
        self.connectionPort = CoordinateState(self, [243,153,21])
        self.connectionPort.pack(side = LEFT)

if __name__ == '__main__':
    pass
