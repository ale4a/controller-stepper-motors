import tkinter as tk
import components.Arduino as Arduino

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.moving = False
        self.move_delay = 50
        self.arduino = Arduino.Arduino("COM4")

        self.after(self.move_delay, self.move)
        
        self.button = tk.Button(self, text="Hold to start movement", command=self.move)
        self.button.pack(side="top")

        self.button.bind("<ButtonPress>", self.on_press)
        self.button.bind("<ButtonRelease>", self.on_release)

    def move(self):
        if self.moving:
            self.arduino.constansMove()
        self.after(-1, self.move)
        
    def on_press(self, event):
        self.moving = True

    def on_release(self, event):
        self.moving = False

if __name__ == '__main__':
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()