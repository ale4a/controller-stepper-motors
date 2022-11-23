# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT, END, CENTER
from tkinter import Tk, Label
from tkinter import Frame, Button, Entry, StringVar
import components.Messages as Messages
import tkinter.font as font
from tkinter.ttk import Combobox
import utils.convert as Convert
from constants.constants import MILLIMITERS, STEPS
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z
from constants.constants import POSITIVE, NEGATIVE
import utils.convert as Convert

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
            MILLIMITERS,
            STEPS
        ]
        self.stepsValueAxisX =  StringVar()
        self.stepsValueAxisY =  StringVar()
        self.stepsValueAxisZ =  StringVar()
        self.totalStepsAxisX = 1
        self.totalStepsAxisY = 1
        self.totalStepsAxisZ = 1
        self.createWidgets()

    def relativeMovement(self, axis, steps):
        measure = self.measuramentComoboboxValue.get()
        res = "R"+ ";" + axis + ";" + str(steps) + ";" + measure
        try:
            stateAnswer = self.arduino.readOptions(res)
            if(not stateAnswer):
                self.messages.popupShowinfo("Error", "Invalid input")
        except Exception as e:
            self.messages.popupShowinfo("Error", e)

    def movementAxis(self, axis, direction):
        if(axis == AXIS_X):
            if direction == POSITIVE:
                self.relativeMovement("X",self.totalStepsAxisX)
            else:
                self.relativeMovement("X",-self.totalStepsAxisX)
        elif(axis == AXIS_Y):
            if direction == POSITIVE:
                self.relativeMovement("Y",self.totalStepsAxisY)
            else:
                self.relativeMovement("Y",-self.totalStepsAxisY)
        elif(axis == AXIS_Z):
            if direction == POSITIVE:
                self.relativeMovement("Z",self.totalStepsAxisZ)
            else:
                self.relativeMovement("Z",-self.totalStepsAxisZ)
                
    def sendCommand(self):
        self.arduino.setZeroPosition()
    
    def resetEntryValuesToSteps(self):
        self.totalStepsAxisX = 10
        self.totalStepsAxisY = 10
        self.totalStepsAxisZ = 10
        self.stepsValueAxisXEntry.delete(0, END)
        self.stepsValueAxisYEntry.delete(0, END)
        self.stepsValueAxisZEntry.delete(0, END)
        self.stepsValueAxisXEntry.insert(0, self.totalStepsAxisX)
        self.stepsValueAxisYEntry.insert(0, self.totalStepsAxisY)
        self.stepsValueAxisZEntry.insert(0, self.totalStepsAxisZ)

    def comoboboxChangeMeasurament(self, event):
        if (self.measuramentComoboboxValue.get() == STEPS):
            self.resetEntryValuesToSteps()

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
        rateComobobox.grid(row = 0, column = 3)
        rateComobobox['values'] = self.measurements
        rateComobobox.current(0)
        rateComobobox.bind('<<ComboboxSelected>>', self.comoboboxChangeMeasurament)

        # ---------------------------------------------- X
        self.axisXValue = Label(self.parent, text = "X:", font=fontState)
        self.axisXValue.grid(row = 1, column = 0, **padding)

        self.rightButton = Button(self.parent, text="-", command = lambda: self.movementAxis(AXIS_X, NEGATIVE), **stylesOptions)
        self.rightButton.grid(row = 1, column = 1, **padding)

        self.stepsValueAxisX.trace("w", lambda name, index, mode, sv=self.stepsValueAxisX: self.updateStepAxisXCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepsValueAxisXEntry = Entry(self.parent, textvariable = self.stepsValueAxisX, validatecommand=(vcmd, '%P'), **defaultValuesEntry)
        self.stepsValueAxisXEntry.insert ( END, self.totalStepsAxisX )
        self.stepsValueAxisXEntry.grid(row = 1, column = 2, **padding)

        self.leftButton = Button(self.parent, text="+", command=lambda: self.movementAxis(AXIS_X, POSITIVE), **stylesOptions)
        self.leftButton.grid(row = 1, column = 3, **padding)

        # ---------------------------------------------- Y
        self.axisXValue = Label(self.parent, text = "Y:", font=fontState)
        self.axisXValue.grid(row = 2, column = 0, **padding)

        self.downButton = Button(self.parent, text="-", command= lambda: self.movementAxis(AXIS_Y, NEGATIVE), **stylesOptions)
        self.downButton.grid(row = 2, column = 1, **padding)

        self.stepsValueAxisY.trace("w", lambda name, index, mode, sv=self.stepsValueAxisY: self.updateStepAxisYCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepsValueAxisYEntry = Entry(self.parent,  textvariable = self.stepsValueAxisY, validatecommand=(vcmd, '%P'), **defaultValuesEntry)
        self.stepsValueAxisYEntry.insert ( END, self.totalStepsAxisY )
        self.stepsValueAxisYEntry.grid(row = 2, column = 2, **padding)

        self.yAxisPositive = Button(self.parent, text="+", command= lambda: self.movementAxis(AXIS_Y, POSITIVE), **stylesOptions)
        self.yAxisPositive.grid(row = 2, column = 3, **padding)

        # ---------------------------------------------- Z
        self.axisXValue = Label(self.parent, text = "Z:", font=fontState)
        self.axisXValue.grid(row = 3, column = 0, **padding)

        self.leftButton = Button(self.parent, text="-", command=lambda: self.movementAxis(AXIS_Z, NEGATIVE), **stylesOptions)
        self.leftButton.grid(row = 3, column = 1, **padding)

        self.stepsValueAxisZ.trace("w", lambda name, index, mode, sv=self.stepsValueAxisZ: self.updateStepAxisZCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepsValueAxisZEntry = Entry(self.parent,  textvariable = self.stepsValueAxisZ, validatecommand=(vcmd, '%P'), **defaultValuesEntry)
        self.stepsValueAxisZEntry.insert (END, self.totalStepsAxisZ )
        self.stepsValueAxisZEntry.grid(row = 3, column = 2, **padding)

        self.leftButton = Button(self.parent, text="+", command=lambda: self.movementAxis(AXIS_Z, POSITIVE), **stylesOptions)
        self.leftButton.grid(row = 3, column = 3, **padding)

    def updateStepAxisXCallback(self, sev):
        if not self.stepsValueAxisX.get()=='':
            self.totalStepsAxisX = Convert.convertStringToNumber(self.stepsValueAxisX.get())

    def updateStepAxisYCallback(self, sev):
        if not self.stepsValueAxisY.get()=='':
            self.totalStepsAxisY = Convert.convertStringToNumber(self.stepsValueAxisY.get())

    def updateStepAxisZCallback(self, sev):
        if not self.stepsValueAxisZ.get()=='':
            self.totalStepsAxisZ = Convert.convertStringToNumber(self.stepsValueAxisZ.get())
    
    def validationOnlyNumbers(self, P):
        if (self.measuramentComoboboxValue.get() == STEPS):
            return str.isdigit(P) or P == ""
        return Convert.isNumber(P) or P == ""
        
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
