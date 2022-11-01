import tkinter as tk
from tkinter import ttk
import components.ConnectionPort as ConnectionPort
import components.CommandsConsole as CommandsConsole
import components.ArduinoController as ArduinoController
import components.ArrowControl as ArrowControl
import components.CoordinateState as CoordinateState

class Counter_program():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Steps Motors")
        self.absPosition = [0, 0, 0]
        self.fromlist_frame = ttk.LabelFrame(self.window, text="Absolute position", relief=tk.RIDGE)
        self.statusDisplay = CoordinateState.CoordinateState(self.fromlist_frame, self.absPosition)
        self.arduino = ArduinoController.ArduinoController(self.absPosition, self.statusDisplay)
        self.radio_variable = tk.StringVar()
        self.combobox_value = tk.StringVar()
        self.create_widgets()

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
        # The Data entry frame
        commandsConsoleFrame = ttk.LabelFrame(self.window, text="Commands console", relief=tk.RIDGE)
        CommandsConsole.CommandsConsole(commandsConsoleFrame, self.arduino)
        commandsConsoleFrame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # - - - - - - - - - - - - - - - - - - - - -
        # The Choosing from lists frame
        self.fromlist_frame.grid(row=1, column=2, sticky=tk.E + tk.W + tk.N + tk.S, padx=6)
        
        # - - - - - - - - - - - - - - - - - - - - -
        # Direcctions
        arrowControlFrame = ttk.LabelFrame(self.window, text="Arrow control", relief=tk.RIDGE, padding=6)
        ArrowControl.ArrowControl(arrowControlFrame, self.arduino)
        arrowControlFrame.grid(row=2, column=2, padx=6, sticky=tk.E + tk.W + tk.N + tk.S)

# Create the entire GUI program
program = Counter_program()

# Start the GUI event loop
program.window.mainloop()