# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, NORMAL , DISABLED, LEFT, END, W
from tkinter import Tk, Label, Entry
from tkinter import Frame, Text, Button

class CommandsConsole(Frame):
    def __init__(self, parent, arduino):
        super().__init__()
        self.arduino = arduino
        self.parent = parent
        self.createWidgets()

    def sendCommand(self):
        self.commandToSend = self.inputCommand.get()
        self.textCommand.config(state=NORMAL)
        self.textCommand.insert(END, ">"+self.commandToSend + '\n')
        self.arduino.readOptions(self.commandToSend)
        stateAnswer = self.arduino.readOptions(self.commandToSend)
        if(stateAnswer != True):
            self.textCommand.insert(END, "Invalid input.\n")
        else:
            print(stateAnswer)
        self.textCommand.config(state=DISABLED)
        self.inputCommand.delete(0, END)

    def sendCommandWithEnter(self, env):
        self.commandToSend = self.inputCommand.get()
        self.textCommand.config(state=NORMAL)
        self.textCommand.insert(END, ">"+self.commandToSend + '\n')
        stateAnswer = self.arduino.readOptions(self.commandToSend)
        if(stateAnswer != True):
            self.textCommand.insert(END, "Invalid input.\n")
        else:
            print(stateAnswer)
        self.textCommand.config(state=DISABLED)
        self.inputCommand.delete(0, END)

    def createWidgets(self):
        commandLabel = Label(self.parent, text="Command:")
        commandLabel.grid(row = 0, column = 0)

        self.inputCommand = Entry(self.parent, width = 70)
        self.inputCommand.grid(row = 0, column = 1)
        
        self.inputCommand.bind("<Return>", self.sendCommandWithEnter)

        self.sendButton = Button(self.parent, text= "Send", command = self.sendCommand, width=20)
        self.sendButton.grid(row = 0, column = 2, sticky=W)

        self.textCommand = Text(self.parent, state=DISABLED, height=10)
        self.textCommand.grid(row = 1, column = 0, columnspan=3, pady=8)

class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x500")
        self.parent.title('Software to scanner')
        self.connectionPort = CommandsConsole(self, self.arduino)
        self.connectionPort.pack(side = LEFT)


if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application