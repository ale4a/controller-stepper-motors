import tkinter as tk
from tkinter.messagebox import showinfo

# --- classes ---
class Messages():

    def __init__(self):
        root = tk.Tk()

        button_showinfo = tk.Button(root, text="ShowInfo", command=self.popup_showinfo)
        button_showinfo.pack(fill='x')

        root.mainloop()

    def popupShowinfo(self):
        showinfo("ShowInfo", "Hello World!")

# --- main ---
