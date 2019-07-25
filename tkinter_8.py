# Binding a function to a widget: command and event

from tkinter import *


class owo:
    def __init__(self, master):     # master is the main window: when you first create an object of this class, make a root/main window
        frame = Frame(master)
        frame.pack(width=200, height=200)

window = Tk()
window.geometry('200x100')



window.mainloop()
