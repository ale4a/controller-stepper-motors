# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LEFT, END
from tkinter import Tk, Label
from tkinter import Frame, Button, Entry

class ArrowControl(Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.createWidgets()

    def yPositive(self):
        print("yPositive")

    def yNegative(self):
        print("yNegative")

    def xPositive(self):
        print("xPositive")

    def xNegative(self):
        print("xNegative")
    
    def zPositive(self):
        print("zPositive")
    
    def zNegative(self):
        print("zNegative")
    
    def createWidgets(self):
        padding = {"padx": 5, "pady": 5}
        self.upButton = Button(self.parent, text="+y", command=self.yPositive, width=5, height=2)
        self.upButton.grid(row = 0, column = 1, **padding)

        self.downButton = Button(self.parent, text="-y", command=self.yNegative, width=5, height=2)
        self.downButton.grid(row = 1, column = 1, **padding)

        self.rightButton = Button(self.parent, text="-x", command=self.xNegative, width=5, height=2)
        self.rightButton.grid(row = 1, column = 0, **padding)

        self.leftButton = Button(self.parent, text="+x", command=self.xPositive, width=5, height=2)
        self.leftButton.grid(row = 1, column = 2, **padding)

        self.leftButton = Button(self.parent, text="+z", command=self.zPositive, width=5, height=2)
        self.leftButton.grid(row = 0, column = 4, **padding)

        self.leftButton = Button(self.parent, text="-z", command=self.zNegative, width=5, height=2)
        self.leftButton.grid(row = 1, column = 4, **padding)

        self.stepLabel = Label(self.parent, text = "Steps")
        self.stepLabel.grid(row = 3, column = 0)

        self.stepEntry = Entry(self.parent, width=8, text="0.1")
        self.stepEntry.insert ( END, "0.1" )
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
