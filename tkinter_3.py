from tkinter import *

window = Tk()
window.title("Edureka")

one = Label(window, text="One", bg="red", fg="white")
one.pack()

two = Label(window, text="Two", bg="green", fg="white")
two.pack(fill=X)        # we want to fill it as long as the X value of the parent

three = Label(window, text="Three", bg="blue", fg="white")
three.pack(side=LEFT, fill=Y)

window.mainloop()
