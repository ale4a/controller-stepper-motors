# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, LabelFrame, Label, StringVar, W
from tkinter import Frame, OptionMenu

class ConectionPort(Frame):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.createWidgets()

    def createWidgets(self):
        self.connectionContainer = LabelFrame(self)
        self.connectionContainer["text"] = "container"
        self.connectionContainer.grid(row = 0, column = 0, columnspan = 3, pady = 10, padx = 10)

        self.portNameLabel = Label(self.connectionContainer)
        self.portNameLabel["text"] = "Port name label:"
        self.portNameLabel.grid(column = 1, row = 1)

        # initialize data
        self.languages = ('Python', 'JavaScript', 'Java',
                        'Swift', 'GoLang', 'C#', 'C++', 'Scala')

        # set up variable
        self.option_var = StringVar(self.connectionContainer)

        # padding for widgets using the grid layout
        paddings = {'padx': 25, 'pady': 25}

        # label
        self.label = Label(self.connectionContainer,  text='Select your most favorite language:')
        self.label.grid(column=0, row=0, sticky=W, **paddings)

        # option menu
        self.option_menu = OptionMenu(
            self.connectionContainer,
            self.option_var,
            self.languages[0],
            *self.languages,
            command=self.option_changed)

        self.option_menu.grid(column=10, row=10, sticky=W, **paddings)

        # output label
        self.output_label = Label(self.connectionContainer, foreground='red')
        self.output_label.grid(column=0, row=1, sticky=W, **paddings)

    def option_changed(self, *args):
        self.output_label['text'] = f'You selected: {self.option_var.get()}'
        
class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x500")
        self.parent.title('Software to scanner')

        self.connectionPort = ConectionPort(self)
        self.connectionPort.pack()


if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application