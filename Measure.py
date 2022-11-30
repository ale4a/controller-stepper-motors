from tkinter import Toplevel
from tkinter import PhotoImage, Button
from tkinter import Label
import tkinter.font as font
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
        self.parent.geometry("200x180")
        self.create_widgets()

    def movePositiveAxisX(self):
        if self.movingPositiveAxisX:
            self.arduino.constantMoveController(AXIS_X, 1)
        if self.movingPositiveAxisY:
            self.arduino.constantMoveController(AXIS_Y, 1)
        if self.movingPositiveAxisZ:
            self.arduino.constantMoveController(AXIS_Z, 1)

        self.parent.after(1, self.movePositiveAxisX)
    
    def moveNegativeAxisX(self):
        if self.movingNegativeAxisX:
            self.arduino.constantMoveController(AXIS_X, -1)
        if self.movingNegativeAxisY:
            self.arduino.constantMoveController(AXIS_Y, -1)
        if self.movingNegativeAxisZ:
            self.arduino.constantMoveController(AXIS_Z, -1)
            
        self.parent.after(1, self.moveNegativeAxisX)

    def create_widgets(self):
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
        # ---------------------------------------------- X
        self.axisYValue = Label(self.parent, text = "X:", font=fontState)
        self.axisYValue.grid(row = 0, column = 0, **padding)
        self.switchAxisNegativeX = Button(self.parent, text="-", **stylesOptions)
        self.switchAxisNegativeX.grid(row = 0, column = 1, **padding)
        self.switchAxisNegativeX.after(self.move_delay, self.moveNegativeAxisX)
        self.switchAxisNegativeX.bind("<ButtonPress>", lambda event : self.on_press(AXIS_X, -1, event))
        self.switchAxisNegativeX.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_X, -1, event))
        self.switchAxisPositiveX = Button(self.parent, text="+", **stylesOptions)
        self.switchAxisPositiveX.grid(row = 0, column = 2, **padding)
        self.switchAxisPositiveX.after(self.move_delay, self.movePositiveAxisX)
        self.switchAxisPositiveX.bind("<ButtonPress>", lambda event : self.on_press(AXIS_X, 1, event))
        self.switchAxisPositiveX.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_X, 1, event))

        # ---------------------------------------------- Y
        self.axisYValue = Label(self.parent, text = "Y:", font=fontState)
        self.axisYValue.grid(row = 1, column = 0, **padding)
        self.switchAxisNegativeY = Button(self.parent, text="-", **stylesOptions)
        self.switchAxisNegativeY.grid(row = 1, column = 1, **padding)
        self.switchAxisNegativeY.after(self.move_delay, self.moveNegativeAxisX)
        self.switchAxisNegativeY.bind("<ButtonPress>", lambda event : self.on_press(AXIS_Y, -1, event))
        self.switchAxisNegativeY.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_Y, -1, event))
        self.switchAxisPositiveY = Button(self.parent, text="+", **stylesOptions)
        self.switchAxisPositiveY.grid(row = 1, column = 2, **padding)
        self.switchAxisPositiveY.after(self.move_delay, self.movePositiveAxisX)
        self.switchAxisPositiveY.bind("<ButtonPress>", lambda event : self.on_press(AXIS_Y, 1, event))
        self.switchAxisPositiveY.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_Y, 1, event))
        # ---------------------------------------------- Z
        
        self.axisYValue = Label(self.parent, text = "Z:", font=fontState)
        self.axisYValue.grid(row = 2, column = 0, **padding)
        self.switchAxisNegativeY = Button(self.parent, text="-", **stylesOptions)
        self.switchAxisNegativeY.grid(row = 2, column = 1, **padding)
        self.switchAxisNegativeY.after(self.move_delay, self.moveNegativeAxisX)
        self.switchAxisNegativeY.bind("<ButtonPress>", lambda event : self.on_press(AXIS_Z, -1, event))
        self.switchAxisNegativeY.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_Z, -1, event))
        self.switchAxisPositiveY = Button(self.parent, text="+", **stylesOptions)
        self.switchAxisPositiveY.grid(row = 2, column = 2, **padding)
        self.switchAxisPositiveY.after(self.move_delay, self.movePositiveAxisX)
        self.switchAxisPositiveY.bind("<ButtonPress>", lambda event : self.on_press(AXIS_Z, 1, event))
        self.switchAxisPositiveY.bind("<ButtonRelease>", lambda event : self.on_release(AXIS_Z, 1, event))

    def on_press(self, axis, direction, event):
        if(axis == AXIS_X):
            if(direction > 0):
                self.movingPositiveAxisX = True
            else:
                self.movingNegativeAxisX = True
        if(axis == AXIS_Y):
            if(direction > 0):
                self.movingPositiveAxisY = True
            else:
                self.movingNegativeAxisY = True
        if(axis == AXIS_Z):
            if(direction > 0):
                self.movingPositiveAxisZ = True
            else:
                self.movingNegativeAxisZ = True

    def on_release(self, axis, direction, event):
        if(axis == AXIS_X):
            if(direction > 0):
                self.movingPositiveAxisX = False
            else:
                self.movingNegativeAxisX = False
        if(axis == AXIS_Y):
            if(direction > 0):
                self.movingPositiveAxisY = False
            else:
                self.movingNegativeAxisY = False
        if(axis == AXIS_Z):
            if(direction > 0):
                self.movingPositiveAxisZ = False
            else:
                self.movingNegativeAxisZ = False

if __name__ == '__main__':
    pass
