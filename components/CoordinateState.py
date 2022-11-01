# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT
from tkinter import Tk, Label
from tkinter import Frame

class CoordinateState(Frame):
    def __init__(self, parent, absPosition):
        super().__init__()
        self.parent = parent
        self.absPosition = absPosition
        self.createWidgets()

    def updateAxis(self):
        self.axisXValue.config(text = str(self.absPosition[0]))
        self.axisYValue.config(text = str(self.absPosition[1]))
        self.axisZValue.config(text = str(self.absPosition[2]))

    def createWidgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {"pady": 5, "padx":15}
        stylesLabel = {
            "bg": "white", 
            "width": 15
        }
        messuare = "steps"
        # - - - - - - - - - - - - - - - - - - - - -
        # Axis X
        self.axisXLabel = Label(self.parent, text="X:", font=fontState)
        self.axisXLabel.grid(row = 0, column = 0, **padding)

        self.axisXValue = Label(self.parent, text = str(self.absPosition[0]), font=fontState, **stylesLabel)
        self.axisXValue.grid(row = 0, column = 1, **padding)

        self.axisXMessuare = Label(self.parent, text = messuare, font=fontState)
        self.axisXMessuare.grid(row = 0, column = 2, **padding)

        # - - - - - - - - - - - - - - - - - - - - -
        # Axis Y

        self.axisYLabel = Label(self.parent, text="Y:", font=fontState)
        self.axisYLabel.grid(row = 1, column = 0,  **padding)

        self.axisYValue = Label(self.parent, text = str(self.absPosition[1]), font=fontState, **stylesLabel)
        self.axisYValue.grid(row = 1, column = 1, **padding)

        self.axisYMessuare = Label(self.parent, text = messuare, font=fontState)
        self.axisYMessuare.grid(row = 1, column = 2, **padding)

        # - - - - - - - - - - - - - - - - - - - - -
        # Axis Z

        self.axisZLabel = Label(self.parent, text="Z:", font=fontState)
        self.axisZLabel.grid(row = 2, column = 0, **padding)

        self.axisZValue = Label(self.parent, text = str(self.absPosition[2]), font=fontState, **stylesLabel)
        self.axisZValue.grid(row = 2, column = 1, **padding)

        self.axisZMessuare = Label(self.parent, text = messuare, font=fontState)
        self.axisZMessuare.grid(row = 2, column = 2, **padding)


class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x500")
        self.parent.title('Software to scanner')
        self.connectionPort = CoordinateState(self, [243,153,21])
        self.connectionPort.pack(side = LEFT)

if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
