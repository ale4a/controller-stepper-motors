



# Use Tkinter for python 2, tkinter for python 3
from distutils.spawn import spawn
from tkinter import Tk, RIGHT, NORMAL , DISABLED, LEFT, END, INSERT
from tkinter import Tk, LabelFrame, Label, Entry, W
from tkinter import Frame, Text, Button

import sys
import glob
import serial
import time



class CommandControl(Frame):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.createWidgets()

    def sendCommand(self):
        self.commandToSend = self.inputCommand.get()
        self.textCommand.config(state=NORMAL)
        self.textCommand.insert(END, ">"+self.commandToSend + '\n')
        self.textCommand.config(state=DISABLED)
        self.inputCommand.delete(0, END)

    def sendCommandWithEnter(self, event):
        self.commandToSend = self.inputCommand.get()
        self.textCommand.config(state=NORMAL)
        self.textCommand.insert(END, ">"+self.commandToSend + '\n')
        self.textCommand.config(state=DISABLED)
        self.inputCommand.delete(0, END)


    def createWidgets(self):
        self.commandContainer = LabelFrame(self)
        self.commandContainer["text"] = " Command "
        self.commandContainer.grid(row = 0, column = 0, columnspan = 5, pady = 10, padx = 10)

        commandLabel = Label(self.commandContainer, text="User Name")
        commandLabel.grid(row = 0, column = 0)

        self.inputCommand = Entry(self.commandContainer, width = 50)
        self.inputCommand.grid(row = 0, column = 1)
        
        self.inputCommand.bind("<Return>", self.sendCommandWithEnter)

        self.sendButton = Button(self.commandContainer, text= "Send", command = self.sendCommand)
        self.sendButton.grid(row = 0, column = 2)

        self.textCommand = Text(self.commandContainer, state=DISABLED)
        self.textCommand.grid(row = 3, column = 1)

        
        
class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x500")
        self.parent.title('Software to scanner')

        self.connectionPort = CommandControl(self)
        self.connectionPort.pack(side = LEFT)


if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

