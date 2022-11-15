
from tkinter import *
root = Tk()
root.geometry("500x300")


isConnected = False
 
def switchConnection():
    global isConnected
    if isConnected:
        switchConnection.config(image = offImage)
        isConnected = False
    else:
        switchConnection.config(image = onImage)
        isConnected = True
 
onImage = PhotoImage(file = "img/on.png")
offImage = PhotoImage(file = "img/off.png")
 
switchConnection = Button(root, image = offImage, bd = 0, command = switchConnection)
switchConnection.pack(pady = 50)
 
root.mainloop()