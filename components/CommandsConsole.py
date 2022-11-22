# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, NORMAL , DISABLED, LEFT, END, W
from tkinter import Tk, Label, Entry
from tkinter import Frame, Button
from tkinter import scrolledtext
import components.Messages as Messages
import utils.convert as Convert
from constants.constants import MILLIMITERS
class CommandsConsole(Frame):
    def __init__(self, parent, arduino):
        super().__init__()
        self.arduino = arduino
        self.parent = parent
        self.messages = Messages.Messages()
        self.createWidgets()

    def cleanText(self):
        self.textCommand.config(state=NORMAL)
        self.textCommand.delete(1.0, END)
        self.textCommand.config(state=DISABLED)

    def sendCommand(self):
        try:
            self.commandToSend = self.inputCommand.get() + ";" + MILLIMITERS
            self.textCommand.insert(END, "> "+self.commandToSend + '\n')
            self.textCommand.config(state=NORMAL)
            stateAnswer = self.arduino.readOptions(self.commandToSend)
            if(stateAnswer != True):
                self.textCommand.insert(END, "Invalid input.\n")
            self.textCommand.config(state=DISABLED)
        except Exception as e:
            self.messages.popupShowinfo("Error", "Problems with arduino connection")
        finally: 
            self.inputCommand.delete(0, END)


    def sendCommandWithEnter(self, env):
        try:
            self.commandToSend = self.inputCommand.get() + ";" + MILLIMITERS
            self.textCommand.config(state=NORMAL)
            self.textCommand.insert(END, "> "+self.commandToSend + '\n')
            stateAnswer = self.arduino.readOptions(self.commandToSend)
            if(stateAnswer != True):
                self.textCommand.insert(END, "Invalid input.\n")
                self.messages.popupShowinfo("Error", "Invalid input")
            self.textCommand.config(state=DISABLED)
        except Exception as e:
            self.messages.popupShowinfo("Error", "Problems with arduino connection")
        finally: 
            self.inputCommand.delete(0, END)

    def createWidgets(self):
        commandLabel = Label(self.parent, text="Command:")
        commandLabel.grid(row = 0, column = 0)

        self.inputCommand = Entry(self.parent, width =25)
        self.inputCommand.grid(row = 0, column = 1)
        self.inputCommand.bind("<Return>", self.sendCommandWithEnter)

        self.sendButton = Button(self.parent, text= "Send", command = self.sendCommand, width=8)
        self.sendButton.grid(row = 0, column = 2, sticky=W)

        self.cleanButton = Button(self.parent, text= "Clean", command = self.cleanText, width=8)
        self.cleanButton.grid(row = 0, column = 3, sticky=W)

        self.textCommand = scrolledtext.ScrolledText(self.parent, state=DISABLED, width=45, height=10)
        self.textCommand.grid(row = 1, column = 0, columnspan=4, pady=8)

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
