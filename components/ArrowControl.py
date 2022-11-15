# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT, END, CENTER
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
        self.absPosition = [0, 0, 0]
        self.messages = Messages.Messages()
        self.measurements = [
            "steps",
            "mm"
        ]
        self.stepsValueAxisX =  StringVar()
        self.stepsValueAxisY =  StringVar()
        self.stepsValueAxisZ =  StringVar()
        self.totalStepsAxisX = 100
        self.totalStepsAxisY = 100
        self.totalStepsAxisZ = 100
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
        self.relativeMovement("Y",self.totalStepsAxisY)

    def yNegative(self):
        self.relativeMovement("Y",-self.totalStepsAxisY)

    def xPositive(self):
        self.relativeMovement("X",self.totalStepsAxisX)

    def xNegative(self):
        self.relativeMovement("X",-self.totalStepsAxisX)
    
    def zPositive(self):
        self.relativeMovement("Z",self.totalStepsAxisZ)
    
    def zNegative(self):
        self.relativeMovement("Z",-self.totalStepsAxisZ)
    
    def sendCommand(self):
        self.arduino.setZeroPosition()
        
    def createWidgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {
            "padx": 2, 
            "pady": 15
        }
        stylesOptions = {
            "width": 4,
            "bg": "#253D5B",
            "fg": "white",
            "font": font.Font(size=8)
        }
        defaultValuesEntry = {
            "justify": CENTER,
            "width": 12, 
            "validate": 'all'
        }

        self.sendButton = Button(self.parent, text= "Set position",command = self.sendCommand, width=15)
        self.sendButton.grid(row = 0, column = 0, columnspan=3)

        self.measuramentComoboboxValue = StringVar()
        rateComobobox = Combobox(self.parent, height=4, width = 5, textvariable=self.measuramentComoboboxValue, justify=CENTER)
        rateComobobox.grid(row = 0, column = 3, columnspan=2)
        rateComobobox['values'] = self.measurements
        rateComobobox.current(0)

        # ---------------------------------------------- X
        self.axisXValue = Label(self.parent, text = "X:", font=fontState)
        self.axisXValue.grid(row = 1, column = 0, **padding)

        self.rightButton = Button(self.parent, text="-", command=self.xNegative, **stylesOptions)
        self.rightButton.grid(row = 1, column = 1, **padding)

        self.stepsValueAxisX.trace("w", lambda name, index, mode, sv=self.stepsValueAxisX: self.updateStepAxisXCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepsValueAxisXEntry = Entry(self.parent, textvariable = self.stepsValueAxisX, validatecommand=(vcmd, '%P'), **defaultValuesEntry)
        self.stepsValueAxisXEntry.insert ( END, self.totalStepsAxisX )
        self.stepsValueAxisXEntry.grid(row = 1, column = 2, **padding)

        self.leftButton = Button(self.parent, text="+", command=self.xPositive, **stylesOptions)
        self.leftButton.grid(row = 1, column = 3, **padding)

        # ---------------------------------------------- Y
        self.axisXValue = Label(self.parent, text = "Y:", font=fontState)
        self.axisXValue.grid(row = 2, column = 0, **padding)

        self.downButton = Button(self.parent, text="-", command=self.yNegative, **stylesOptions)
        self.downButton.grid(row = 2, column = 1, **padding)

        self.stepsValueAxisY.trace("w", lambda name, index, mode, sv=self.stepsValueAxisY: self.updateStepAxisYCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepsValueAxisYEntry = Entry(self.parent,  textvariable = self.stepsValueAxisY, validatecommand=(vcmd, '%P'), **defaultValuesEntry)
        self.stepsValueAxisYEntry.insert ( END, self.totalStepsAxisY )
        self.stepsValueAxisYEntry.grid(row = 2, column = 2, **padding)

        self.yAxisPositive = Button(self.parent, text="+", command=self.yPositive, **stylesOptions)
        self.yAxisPositive.grid(row = 2, column = 3, **padding)

        self.axisXValue = Label(self.parent, text = "Z:", font=fontState)
        self.axisXValue.grid(row = 3, column = 0, **padding)

        self.leftButton = Button(self.parent, text="-", command=self.zNegative, **stylesOptions)
        self.leftButton.grid(row = 3, column = 1, **padding)

        # ---------------------------------------------- Z
        self.stepsValueAxisZ.trace("w", lambda name, index, mode, sv=self.stepsValueAxisZ: self.updateStepAxisZCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepsValueAxisZEntry = Entry(self.parent,  textvariable = self.stepsValueAxisZ, validatecommand=(vcmd, '%P'), **defaultValuesEntry)
        self.stepsValueAxisZEntry.insert (END, self.totalStepsAxisZ )
        self.stepsValueAxisZEntry.grid(row = 3, column = 2, **padding)

        self.leftButton = Button(self.parent, text="+", command=self.zPositive, **stylesOptions)
        self.leftButton.grid(row = 3, column = 3, **padding)

    def updateStepAxisXCallback(self, sev):
        if not self.stepsValueAxisX.get()=='':
            self.totalStepsAxisX = int(self.stepsValueAxisX.get())

    def updateStepAxisYCallback(self, sev):
        if not self.stepsValueAxisY.get()=='':
            self.totalStepsAxisY = int(self.stepsValueAxisY.get())

    def updateStepAxisZCallback(self, sev):
        if not self.stepsValueAxisZ.get()=='':
            self.totalStepsAxisZ = int(self.stepsValueAxisZ.get())
    
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
