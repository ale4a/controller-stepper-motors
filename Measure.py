from tkinter import Toplevel
from tkinter import PhotoImage, Button
from tkinter import Label
from constants.constants import AXIS_X, AXIS_Y, AXIS_Z

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
        self.parent.geometry("400x400")
        self.create_widgets()

    def movePositiveAxisX(self):
        if self.movingPositiveAxisX:
            self.arduino.constansMoveController(AXIS_X, 1)
        if self.movingPositiveAxisY:
            self.arduino.constansMoveController(AXIS_Y, 1)

        self.switchAxisPositiveX.after(1, self.movePositiveAxisX)
        # self.switchAxisPositiveY.after(1, self.movePositiveAxisX)
        # self.switchAxisPositiveZ.after(1, self.movePositiveAxisX)
    
    def moveNegativeAxisX(self):
        if self.movingNegativeAxisX:
            self.arduino.constansMoveController(AXIS_X, -1)
        if self.movingNegativeAxisY:
            self.arduino.constansMoveController(AXIS_Y, -1)
            
        self.switchAxisNegativeX.after(1, self.moveNegativeAxisX)
        # self.switchAxisNegativeY.after(1, self.moveNegativeAxisX)
        # self.switchAxisNegativeZ.after(1, self.moveNegativeAxisX)

    def create_widgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {
            "padx": 20, 
            "pady": 10
        }
        # ---------------------------------------------- X
        self.axisYValue = Label(self.parent, text = "X:", font=fontState)
        self.axisYValue.grid(row = 0, column = 0, **padding)
        self.switchAxisNegativeX = Button(self.parent, text="-")
        self.switchAxisNegativeX.grid(row = 0, column = 1)
        self.switchAxisNegativeX.after(self.move_delay, self.moveNegativeAxisX)
        self.switchAxisNegativeX.bind("<ButtonPress>", lambda event : self.on_press(AXIS_X, -1, event))
        self.switchAxisNegativeX.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_X, -1, event))
        self.switchAxisPositiveX = Button(self.parent, text="+")
        self.switchAxisPositiveX.grid(row = 0, column = 2)
        self.switchAxisPositiveX.after(self.move_delay, self.movePositiveAxisX)
        self.switchAxisPositiveX.bind("<ButtonPress>", lambda event : self.on_press(AXIS_X, 1, event))
        self.switchAxisPositiveX.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_X, 1, event))

        # ---------------------------------------------- Y
        self.axisYValue = Label(self.parent, text = "Y:", font=fontState)
        self.axisYValue.grid(row = 1, column = 0, **padding)
        self.switchAxisNegativeY = Button(self.parent, text="-")
        self.switchAxisNegativeY.grid(row = 1, column = 1)
        self.switchAxisNegativeY.after(self.move_delay, self.moveNegativeAxisX)
        self.switchAxisNegativeY.bind("<ButtonPress>", lambda event : self.on_press(AXIS_Y, -1, event))
        self.switchAxisNegativeY.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_Y, -1, event))
        self.switchAxisPositiveY = Button(self.parent, text="+")
        self.switchAxisPositiveY.grid(row = 1, column = 2)
        self.switchAxisPositiveY.after(self.move_delay, self.movePositiveAxisX)
        self.switchAxisPositiveY.bind("<ButtonPress>", lambda event : self.on_press(AXIS_Y, 1, event))
        self.switchAxisPositiveY.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_Y, 1, event))
        # ---------------------------------------------- Z
        
        self.axisYValue = Label(self.parent, text = "Y:", font=fontState)
        self.axisYValue.grid(row = 2, column = 0, **padding)

    def on_press(self, axis, direcction, event):
        if(axis == AXIS_X):
            if(direcction > 0):
                self.movingPositiveAxisX = True
            else:
                self.movingNegativeAxisX = True

    def on_release(self, axis, direcction, event):
        if(axis == AXIS_X):
            if(direcction > 0):
                self.movingPositiveAxisX = False
            else:
                self.movingNegativeAxisX = False
