from tkinter import *
from tkinter import ttk
def func():
    l2.configure(text=cb.get())
win =Tk()
win.geometry('200x100')
course=["Java","Python","C & C++"]
l1=Label(win,text="Choose Your Favourite Language")
l1.grid(column=0, row=0)
cb=ttk.Combobox(win,values=course,width=10)
cb.grid(column=0, row=1)
cb.current(0)
print(cb.get())
b=Button(win,text="Click Here",command=func)
b.grid(column=0, row=2)
l2=Label(win,text="")
l2.grid(column=0, row=3)
win.mainloop()