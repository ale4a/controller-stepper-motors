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
        self.isConnectedX = False
        self.isConnectedY = False
        self.isConnectedZ = False

        self.moving = False
        self.move_delay = 50
        
        self.parent.after(self.move_delay, self.movePositiveX)
        # self.parent.after(self.move_delay, self.moveNegativeX)
        self.create_widgets()

    def movePositiveX(self): 
        if self.moving:
            self.arduino.constansMoveController("X",-1)
        self.parent.after(1, self.movePositiveX)

    def moveNegativeX(self):
        if self.moving:
            self.arduino.constansMoveController("X",1)
        self.parent.after(-1, self.moveNegativeX)

    def create_widgets(self):
        fontState  = "Helvetica 10 bold italic"
        padding = {
            "padx": 20, 
            "pady": 20
        }
      
        # ---------------------------------------------- X
        self.axisXValue = Label(self.parent, text = "X:", font=fontState)
        self.axisXValue.grid(row = 0, column = 0, **padding)
        self.switchAxisPositiveX = Button(self.parent, text="+")
        self.switchAxisPositiveX.after(self.move_delay, self.movePositiveX)
        self.switchAxisPositiveX.grid(row = 0, column = 1)
        self.switchAxisPositiveX.bind("<ButtonPress>", self.on_press)
        self.switchAxisPositiveX.bind("<ButtonRelease>", self.on_release)
        # TODO: review why only accept 1 bind
        # self.switchAxisNegativeX = Button(self.parent, text="-")
        # self.switchAxisNegativeX.after(self.move_delay, self.moveNegativeX)
        # self.switchAxisNegativeX.grid(row = 0, column = 2)
        # self.switchAxisNegativeX.bind("<ButtonPress>", self.on_press2)
        # self.switchAxisNegativeX.bind("<ButtonRelease>", self.on_release2)
        
        # ---------------------------------------------- Y
        self.axisXValue = Label(self.parent, text = "Y:", font=fontState)
        self.axisXValue.grid(row = 1, column = 0, **padding)
        # ---------------------------------------------- Z
        self.axisXValue = Label(self.parent, text = "Z:", font=fontState)
        self.axisXValue.grid(row = 2, column = 0, **padding)

    def on_press(self, event):
        self.moving = True

    def on_release(self, event):
        self.moving = False

    def on_press2(self, event):
        self.moving = True

    def on_release2(self, event):
        self.moving = False


    def switchConnectionFuntionX(self):
        if self.isConnectedX:
            self.isConnectedX = False
            self.moving = True
            self.switchAxisPositiveX.config(image = self.offImage)
        else:
            self.isConnectedX = True
            self.moving = False
            self.switchAxisPositiveX.config(image = self.onImage)
