from tkinter import ttk
from tkinter import *

class Conection:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Conection')

        # Creating a frame container
        frame = LabelFrame(self.wind, text = "Connection")
        frame.grid(row = 0, column = 3, columnspan = 30, padx = 30, pady = 30)

        # Name Input
        portNameLabel = Label(frame, text = "Name: ")
        portNameLabel.grid(row = 1, column = 0)
        
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 1)

        # Button
        buttonReload = Button(window,text='Reload', command=onClickReload)
        buttonReload.grid(column=0,row=0)

        portSelectLabel = Label(frame, text = "Replace")

    def onClickReload():

        res = "Welcome to " + txt.get()

        lbl.configure(text= res)

if __name__ == "__main__":
    window = Tk()
    app = Conection(window)
    window.mainloop()
