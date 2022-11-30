import os.path 
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
import components.ConnectionPort as ConnectionPort
import components.CommandsConsole as CommandsConsole
import components.ArduinoControllerSerial as ArduinoControllerSerial
import components.ArduinoController as ArduinoController
import components.ArrowControl as ArrowControl
import components.CoordinateState as CoordinateState
import Measure as Measure
import components.Messages as Messages
from constants.constants import NAME_FILE, SEPARATOR_OPEN_FILE

class ControllerMotors():
    """
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Motor controller")
        self.absPosition = self.readDataFile()
        self.absolutePositionFrame = ttk.LabelFrame(self.window, text="Absolute position", relief=tk.RIDGE)
        self.statusDisplay = CoordinateState.CoordinateState(self.absolutePositionFrame, self.absPosition)
        # This project is using the pyfirmata connection, it is possible to used serial connection enabling ArduinoControllerSerial and comment ArduinoController
        # self.arduino = ArduinoControllerSerial.ArduinoControllerSerial(self.absPosition, self.statusDisplay)
        self.arduino = ArduinoController.ArduinoController(self.absPosition, self.statusDisplay)
        self.messages = Messages.Messages()
        self.measure = Measure.Measure(self.window, self.arduino)
        self.create_widgets()

    def readDataFile(self):
        """readDataFile
            This function read data if there is any current position saved

            Returns
            [axisX, axisY, axisZ] = [int, int, int]
        """
        axisX, axisY, axisZ = (0, 0, 0)
        try:
            if os.path.isfile(NAME_FILE):
                with open(NAME_FILE, "r") as f:
                    lines = f.readlines()
                lines = lines[0].split(SEPARATOR_OPEN_FILE)
                axisX = int(lines[0])
                axisY = int(lines[1])
                axisZ = int(lines[2])
        except:
            print("Error with the file currentPosition.txt")
        return [axisX, axisY, axisZ]

    def writeDataFile(self):
        """writeDataFile
            This function write data about the current position
        """
        file = open(NAME_FILE, "w")
        file.write(str(self.absPosition[0]))
        file.write(SEPARATOR_OPEN_FILE)
        file.write(str(self.absPosition[1]))
        file.write(SEPARATOR_OPEN_FILE)
        file.write(str(self.absPosition[2]))
        file.close()
        
    def openSecondWindow(self):
        if self.measure is not None:
            self.measure = Measure.Measure(self.window, self.arduino)

    def create_widgets(self):
        # Create some room around all the internal frames
        self.window['padx'] = 5
        self.window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The Commands frame
        connectionPortFrame = ttk.LabelFrame(self.window, text="Connection Arduino", relief=tk.RIDGE)
        ConnectionPort.ConnectionPort(connectionPortFrame, self.arduino)
        connectionPortFrame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)
        # - - - - - - - - - - - - - - - - - - - - -
        # The Commands console entry frame
        commandsConsoleFrame = ttk.LabelFrame(self.window, text="Commands console Type ; Axis ; mm", relief=tk.RIDGE)
        CommandsConsole.CommandsConsole(commandsConsoleFrame, self.arduino)
        commandsConsoleFrame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S)
        # - - - - - - - - - - - - - - - - - - - - -
        # The Choosing from lists frame
        self.absolutePositionFrame.grid(row=1, column=2, sticky=tk.E + tk.W + tk.N + tk.S, padx=6)
        # - - - - - - - - - - - - - - - - - - - - -
        # Arrow control entry frame
        arrowControlFrame = ttk.LabelFrame(self.window, text="Arrow control", relief=tk.RIDGE, padding=6)
        ArrowControl.ArrowControl(arrowControlFrame, self.arduino)
        arrowControlFrame.grid(row=2, column=2, padx=6, sticky=tk.E + tk.W + tk.N + tk.S)
        # - - - - - - - - - - - - - - - - - - - - -
        # Menu
        menu = Menu(self.window)
        new_item = Menu(menu, tearoff=0)
        new_item.add_command(label='New', command=self.openSecondWindow)
        menu.add_cascade(label='Second Window', menu=new_item)
        self.window.config(menu=menu)

    def callbackDestroyFirstProgram(self):
        if self.messages.askQuestion("Warning","Do you want to close the program?") == "yes":
            self.writeDataFile()
            program.window.destroy()

if __name__ == "__main__":
    program = ControllerMotors()
    program.window.resizable(False, False)
    program.window.protocol("WM_DELETE_WINDOW",  program.callbackDestroyFirstProgram)
    program.window.mainloop()
    