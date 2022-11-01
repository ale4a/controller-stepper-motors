import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import components.ConnectionPort as ConnectionPort
import components.CommandsConsole as CommandsConsole
import components.ArduinoController as ArduinoController
import components.ArrowControl as ArrowControl

class Counter_program():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Steps Motors")
        self.absPosition = [0, 0, 0]
        self.arduino = ArduinoController.ArduinoController(self.absPosition)
        self.radio_variable = tk.StringVar()
        self.combobox_value = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Create some room around all the internal frames
        self.window['padx'] = 5
        self.window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The Commands frame
        cmd_frame = ttk.LabelFrame(self.window, text="Connection Arduino", relief=tk.RIDGE)
        ConnectionPort.ConnectionPort(cmd_frame, self.arduino)
        cmd_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # - - - - - - - - - - - - - - - - - - - - -
        # The Data entry frame
        entry_frame = ttk.LabelFrame(self.window, text="Commands console", relief=tk.RIDGE)
        CommandsConsole.CommandsConsole(entry_frame, self.arduino)
        entry_frame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S)
        
        # - - - - - - - - - - - - - - - - - - - - -
        # The Choices frame
        switch_frame = ttk.LabelFrame(self.window, text="Direcctions", relief=tk.RIDGE, padding=6)
        ArrowControl.ArrowControl(switch_frame, self.arduino)
        switch_frame.grid(row=2, column=2, padx=6, sticky=tk.E + tk.W + tk.N + tk.S)

        # - - - - - - - - - - - - - - - - - - - - -
        # The Choosing from lists frame
        fromlist_frame = ttk.LabelFrame(self.window, text="Choosing from a list",
                                        relief=tk.RIDGE)
        fromlist_frame.grid(row=1, column=2, sticky=tk.E + tk.W + tk.N + tk.S, padx=6)

        listbox_label = tk.Label(fromlist_frame, text="tk.Listbox")
        listbox_label.grid(row=1, column=1, sticky=tk.W + tk.N)

        combobox_label = tk.Label(fromlist_frame, text="ttk.Combobox")
        combobox_label.grid(row=2, column=1, sticky=tk.W + tk.N)

        my_listbox = tk.Listbox(fromlist_frame, height=4)
        for item in ["one", "two", "three", "four"]:
            my_listbox.insert(tk.END, "Choice " + item)
        my_listbox.grid(row=1, column=2)

        self.combobox_value = tk.StringVar()
        my_combobox = ttk.Combobox(fromlist_frame, height=4, textvariable=self.combobox_value)
        my_combobox.grid(row=2, column=2)
        my_combobox['values'] = ("Choice oneasas", "Choice two", "Choice three", "Choice four")
        my_combobox.current(0)

        # - - - - - - - - - - - - - - - - - - - - -
        # Menus
        # menubar = tk.Menu(self.window)

        # filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Open", command=filedialog.askopenfilename)
        # filemenu.add_command(label="Save", command=filedialog.asksaveasfilename)
        # filemenu.add_separator()
        # filemenu.add_command(label="Exit", command=self.window.quit)
        # menubar.add_cascade(label="File", menu=filemenu)

        # self.window.config(menu=menubar)

        # - - - - - - - - - - - - - - - - - - - - -
        # Quit button in the lower right corner
        # quit_button = ttk.Button(self.window, text="Quit", command=self.window.destroy)
        # quit_button.grid(row=1, column=3)

# Create the entire GUI program
program = Counter_program()

# Start the GUI event loop
program.window.mainloop()