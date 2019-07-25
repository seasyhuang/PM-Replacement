# Binding a function to a widget: command and event

from tkinter import *

window = Tk()
window.geometry('200x100') # Size 200, 100

def printName():
  print("Hello my name is Seasy")

### Command ###
button1 = Button(
    window,
    text="Print name",
    command=printName)      # tells the button the run the function, NO ()


### Event ###
# button1 = Button(window, text="Print name")
# button1.bind("<Button-1>", printName())      # event, function to occur, WITH ()

button1.pack(expand=YES)

window.mainloop()
