# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT, END
from tkinter import Tk, Label
from tkinter import Frame, Button, Entry, StringVar
import components.Messages as Messages
import tkinter.font as font
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
    
    def setPosition(self):
        timeWaitX, timeWaitY, timeWaitZ = self.arduino.getAbsoulutePosition()
        print(timeWaitX, timeWaitY, timeWaitZ)
        # TODO: review the times
        self.absoluteMovement("X", 0)
        time.sleep(3)
        self.absoluteMovement("Y", 0)
        time.sleep(3)
        self.absoluteMovement("Z", 0)
        time.sleep(3)
    
    def createWidgets(self):
        padding = {"padx": 10, "pady": 10}
        stylesOptions = {
            "width": 5,
            "height": 2,
            "bg": "#253D5B",
            "fg": "white",
            "font": font.Font(size=13)
        }
        self.yAxisPositive = Button(self.parent, text="+Y", command=self.yPositive, **stylesOptions)
        self.yAxisPositive.grid(row = 0, column = 1, **padding)

        self.downButton = Button(self.parent, text="-Y", command=self.yNegative, **stylesOptions)
        self.downButton.grid(row = 1, column = 1, **padding)

        self.rightButton = Button(self.parent, text="-X", command=self.xNegative, **stylesOptions)
        self.rightButton.grid(row = 1, column = 0, **padding)

        self.leftButton = Button(self.parent, text="+X", command=self.xPositive, **stylesOptions)
        self.leftButton.grid(row = 1, column = 2, **padding)

        self.leftButton = Button(self.parent, text="+Z", command=self.zPositive, **stylesOptions)
        self.leftButton.grid(row = 0, column = 4, **padding)

        self.leftButton = Button(self.parent, text="-Z", command=self.zNegative, **stylesOptions)
        self.leftButton.grid(row = 1, column = 4, **padding)

        self.stepLabel = Label(self.parent, text = "Steps")
        self.stepLabel.grid(row = 3, column = 0, pady = 20)

        self.steps.trace("w", lambda name, index, mode, sv=self.steps: self.updateStepCallback(sv))
        vcmd = (self.register(self.validationOnlyNumbers))
        self.stepEntry = Entry(self.parent, validate='all', width=8,  textvariable = self.steps, validatecommand=(vcmd, '%P'))
        self.stepEntry.insert ( END, self.totalSteps )
        self.stepEntry.grid(row = 3, column = 1, pady = 20)

        self.leftButton = Button(self.parent, text="Reset position [0, 0, 0]", command=self.setPosition)
        self.leftButton.grid(row = 3, column = 2, **padding, columnspan=3)

    def updateStepCallback(self, sev):
        if not self.steps.get()=='':
            self.totalSteps = int(self.steps.get())

    def validationOnlyNumbers(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
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
