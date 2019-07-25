# Binding a function to a widget: command and event

from tkinter import *

window = Tk()
# window.geometry('200x100')

def leftClick(event):
    print("Left")

def rightClick(event):
    print("Right")

frame = Frame(window, width=300, height=250)

frame.bind("<Button-1>", leftClick)
frame.bind("<Button-3>", rightClick)
frame.pack()

window.mainloop()
