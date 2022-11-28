from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion

"""Messages
    This class help to create messages with options
"""
class Messages():
    def __init__(self):
        pass

    def popupShowinfo(self, title, description):
        showinfo(title, description)
    
    def askQuestion(self, title, description):
        return askquestion(title, description)
        
