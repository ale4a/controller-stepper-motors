from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion

class Messages():
    """
        This class help to create messages in other window with options
    """
    def __init__(self):
        pass

    def popupShowinfo(self, title, description):
        showinfo(title, description)
    
    def askQuestion(self, title, description):
        return askquestion(title, description)
        
if __name__ == '__main__':
    pass
