from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion

class Messages():
    def __init__(self):
        pass

    def popupShowinfo(self, title, description):
        showinfo(title, description)
    
    def askQuestion(self, title, description):
        return askquestion(title, description)
        
