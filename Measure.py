from tkinter import Toplevel
from tkinter import PhotoImage, Button
from tkinter import Tk, Label

class Measure():
    def __init__(self, windowTopLevel, arduino):
        self.windowTopLevel = windowTopLevel
        self.arduino = arduino
        self.onImage = PhotoImage(file = "img/on.png")
        self.offImage = PhotoImage(file = "img/off.png")
        self.parent = Toplevel(self.windowTopLevel)

        self.movingPositiveAxisX = False
        self.movingNegativeAxisX = False

        self.movingPositiveAxisY = False
        self.movingNegativeAxisY = False

        self.movingPositiveAxisZ = False
        self.movingNegativeAxisZ = False
        self.move_delay = 50
        
        self.create_widgets()

    def movePositiveAxisX(self):
        if self.movingPositiveAxisX:
            self.arduino.constansMoveController("X", 1)
        self.switchAxisPositiveX.after(1, self.movePositiveAxisX)
    
    def moveNegativeAxisX(self):
        if self.movingNegativeAxisX:
            self.arduino.constansMoveController("X", -1)
        self.switchAxisNegativeX.after(1, self.moveNegativeAxisX)

    def create_widgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {
            "padx": 20, 
            "pady": 10
        }
      
        # ---------------------------------------------- X
        self.axisXValue = Label(self.parent, text = "X:", font=fontState)
        self.axisXValue.grid(row = 0, column = 0, **padding)

        self.switchAxisNegativeX = Button(self.parent, text="-")
        self.switchAxisNegativeX.grid(row = 0, column = 1)
        self.switchAxisNegativeX.after(self.move_delay, self.moveNegativeAxisX)
        self.switchAxisNegativeX.bind("<ButtonPress>", lambda event : self.on_press("X", -1, event))
        self.switchAxisNegativeX.bind("<ButtonRelease>", lambda event : self.on_release("X", -1, event))

        self.switchAxisPositiveX = Button(self.parent, text="+")
        self.switchAxisPositiveX.grid(row = 0, column = 2)
        self.switchAxisPositiveX.after(self.move_delay, self.movePositiveAxisX)
        self.switchAxisPositiveX.bind("<ButtonPress>", lambda event : self.on_press("X", 1, event))
        self.switchAxisPositiveX.bind("<ButtonRelease>", lambda event : self.on_release("X", 1, event))
        
    def on_press(self, axis, direcction, event):
        if(axis == "X"):
            if(direcction > 0):
                self.movingPositiveAxisX = True
            else:
                self.movingNegativeAxisX = True

    def on_release(self, axis, direcction, event):
        if(axis == "X"):
            if(direcction > 0):
                self.movingPositiveAxisX = False
            else:
                self.movingNegativeAxisX = False
