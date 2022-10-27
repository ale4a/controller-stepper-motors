# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT, END
from tkinter import Tk, Label
from tkinter import Frame, Button, Entry
import tkinter.font as font

class ArrowControl(Frame):
    def __init__(self, parent, arduino):
        super().__init__()
        self.parent = parent
        self.arduino = arduino
        self.steps = 200
        self.createWidgets()

    def relativeMovement(self, axis, steps):
        res = "R"+ ";" + axis + ";" + str(steps)
        try:
            stateAnswer = self.arduino.readOptions(res)
            if(stateAnswer != True):
                self.textCommand.insert(END, "Invalid input.\n")
            else:
                print(stateAnswer)
        except:
            print("error")

    def yPositive(self):
        self.relativeMovement("Y",self.steps)
        print("yPositive")

    def yNegative(self):
        self.relativeMovement("Y",-self.steps)
        print("yNegative")

    def xPositive(self):
        self.relativeMovement("X",self.steps)
        print("xPositive")

    def xNegative(self):
        self.relativeMovement("X",-self.steps)
        print("xNegative")
    
    def zPositive(self):
        self.relativeMovement("Z",self.steps)
        print("zPositive")
    
    def zNegative(self):
        self.relativeMovement("Z",-self.steps)
        print("zNegative")
    
    def createWidgets(self):
        padding = {"padx": 5, "pady": 5}
        stylesOptions = {
            "width": 5,
            "height": 2,
            "bg": "#253D5B",
            "fg": "white",
            "font": font.Font(size=13)
        }
        self.upButton = Button(self.parent, text="+Y", command=self.yPositive, **stylesOptions)
        self.upButton.grid(row = 0, column = 1, **padding)

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
        self.stepLabel.grid(row = 3, column = 0)

        self.stepEntry = Entry(self.parent, width=8)
        self.stepEntry.insert ( END, self.steps )
        self.stepEntry.grid(row = 3, column = 1)
    
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
