import tkinter as tk
import time


class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.moving = False
        self.move_delay = 50
        
        # .after() method is the important function here:
        # It calls self.move() after a certain amount of time (self.move_delay)
        # self.move() is only executed if self.moving flag is set
        # self.moving flag is controlled by on_press() and on_release()
        self.after(self.move_delay, self.move)
        
        self.button = tk.Button(self, text="Hold to start movement")
        self.text = tk.Text(self, width=40, height=6)
        self.vsb = tk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)

        self.textchar = 0

        self.button.pack(side="top")
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="bottom", fill="x")

        self.button.bind("<ButtonPress>", self.on_press)
        self.button.bind("<ButtonRelease>", self.on_release)

    def move(self):
        if self.moving:
            if self.textchar == 0:
                self.text.insert('end', 'Moving')
                self.textchar = 1
            else:
                self.text.insert('end', '.')
        # Here again the self.after() method has to be called
        self.after(self.move_delay, self.move)
        

    def on_press(self, event):
        self.moving = True
        self.button.configure(text='Realease to stop movement')

    def on_release(self, event):
        self.moving = False
        self.textchar = 0
        self.text.insert('end', '\nMovement was stopped\n')
        self.button.configure(text='Hold to start movement')

if __name__ == '__main__':
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()