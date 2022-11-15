# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT, END
from tkinter import Tk, Label
from tkinter import Frame, Button, Entry, StringVar
import components.Messages as Messages
import tkinter.font as font
from tkinter.ttk import Combobox
import time

class ArrowControl(Frame):
    def __init__(self, parent, arduino):
        super().__init__()
        self.parent = parent
        self.arduino = arduino
        self.moving = False
        self.move_delay = 50
        self.steps =  StringVar()
        self.messages = Messages.Messages()
        self.measurements = [
            "steps",
            "mm"
        ]
        self.totalSteps = 100
        self.createWidgets()

    def relativeMovement(self, axis, steps):
        res = "R"+ ";" + axis + ";" + str(steps)
        try:
            stateAnswer = self.arduino.readOptions(res)
            if(not stateAnswer):
                self.textCommand.insert(END, "Invalid input.\n")
                self.messages.popupShowinfo("Error", "Invalid input")
        except Exception as e:
            self.messages.popupShowinfo("Error", e)

    def absoluteMovement(self, axis, steps):
        res = "A"+ ";" + axis + ";" + str(steps)
        try:
            stateAnswer = self.arduino.readOptions(res)
            if(not stateAnswer):
                self.textCommand.insert(END, "Invalid input.\n")
                self.messages.popupShowinfo("Error", "Invalid input")
        except Exception as e:
            print(e)
            self.messages.popupShowinfo("Error", "Problems with connection with arduino")

    def yPositive(self):
        self.relativeMovement("Y",self.totalSteps)

    def yNegative(self):
        self.relativeMovement("Y",-self.totalSteps)

    def xPositive(self):
        self.relativeMovement("X",self.totalSteps)

    def xNegative(self):
        self.relativeMovement("X",-self.totalSteps)
    
    def zPositive(self):
        self.relativeMovement("Z",self.totalSteps)
    
    def zNegative(self):
        self.relativeMovement("Z",-self.totalSteps)
    
    
    def createWidgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {"padx": 5, "pady": 8}
        stylesOptions = {
            "width": 3,
            "bg": "#253D5B",
            "fg": "white",
            "font": font.Font(size=15)
        }

        
        self.measuramentComoboboxValue = StringVar()
        rateComobobox = Combobox(self.parent, height=4, width=5,textvariable=self.measuramentComoboboxValue)
        rateComobobox.grid(row = 1, column = 0, padx=2)
        rateComobobox['values'] = self.measurements
        rateComobobox.current(0)

        self.steps.trace("w", lambda name, index, mode, sv=self.steps: self.updateStepCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepEntry = Entry(self.parent, validate='all', width=8,  textvariable = self.steps, validatecommand=(vcmd, '%P'))
        self.stepEntry.insert ( END, self.totalSteps )
        self.stepEntry.grid(row = 1, column = 1, padx=2)


        self.axisXValue = Label(self.parent, text = "X", font=fontState)
        self.axisXValue.grid(row = 0, column = 2)

        self.rightButton = Button(self.parent, text="-", command=self.xNegative, **stylesOptions)
        self.rightButton.grid(row = 0, column = 3, **padding)

        self.leftButton = Button(self.parent, text="+", command=self.xPositive, **stylesOptions)
        self.leftButton.grid(row = 0, column = 4, **padding)

        self.axisXValue = Label(self.parent, text = "Y", font=fontState)
        self.axisXValue.grid(row = 1, column = 2)

        self.downButton = Button(self.parent, text="-", command=self.yNegative, **stylesOptions)
        self.downButton.grid(row = 1, column = 3, **padding)
        
        self.yAxisPositive = Button(self.parent, text="+", command=self.yPositive, **stylesOptions)
        self.yAxisPositive.grid(row = 1, column = 4, **padding)

        self.axisXValue = Label(self.parent, text = "Z", font=fontState)
        self.axisXValue.grid(row = 2, column = 2)

        self.leftButton = Button(self.parent, text="-", command=self.zNegative, **stylesOptions)
        self.leftButton.grid(row = 2, column = 3, **padding)


        self.leftButton = Button(self.parent, text="+", command=self.zPositive, **stylesOptions)
        self.leftButton.grid(row = 2, column = 4, **padding)


    def updateStepCallback(self, sev):
        if not self.steps.get()=='':
            self.totalSteps = int(self.steps.get())

    def validationOnlyNumbers(self, P):
        return str.isdigit(P) or P == ""
        
class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("500x300")
        self.parent.title('Software to scanner')
        self.connectionPort = ArrowControl(self)
        self.connectionPort.pack(side = LEFT)

if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
