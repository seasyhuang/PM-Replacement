from tkinter import *

window = Tk()

label1 = Label(window, text="Name:")
label2 = Label(window, text="Password:")
entry1 = Entry(window)
entry2 = Entry(window)

# Placing things in a grid
# default is center aligned, STICKY param changes align (NESW)
label1.grid(row=0, column=0, sticky=E)    # default is 0
entry1.grid(row=0, column=1)
label2.grid(row=1, column=0, sticky=E)
entry2.grid(row=1, column=1)

# Check box
check = Checkbutton(window, text="Keep me logged in")
check.grid(columnspan=2)         # makes the button take up 2 columns

window.mainloop()
 
