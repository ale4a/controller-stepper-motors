from tkinter import *
from PIL import ImageTk, Image


import serialPorts

root = Tk()
root.title('Controll 3 step motors')
root.geometry('400x400')

# Drop Down Boxes
def showPort():
    myLabel = Label(root, text = clicked.get()).pack()

options = serialPorts.connect() or []
clicked = StringVar()

drop = OptionMenu(root, clicked, options).pack()
myButton = Button(root, text = "Show port", command = showPort, fg="blue").pack()

root.mainloop()