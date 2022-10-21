from tkinter import Frame, Button, Entry, Label, Tk

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidgets()
    
    def createWidgets(self):
        self.hi_there = Button(self)
        self.hi_there["text"] = 'Hello Wordl\n(click-me)',
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack({"side": "top"})

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.master.destroy
        self.QUIT.pack({"side": "bottom"})

    def say_hi(self):
        print("hi there, everyone!")


if __name__ == "__main__":
    root = Tk()
    Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
