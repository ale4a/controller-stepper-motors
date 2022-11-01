from tkinter.messagebox import showinfo

class Messages():
    def __init__(self):
        pass

    def popupShowinfo(self, title, description):
        showinfo(title, description)
