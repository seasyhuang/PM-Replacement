from tkinter import *

window = Tk()
window.title("Edureka")

# label = Label(window, text="Hello World!").pack()
# # .pack() just packs it in wherever it fits

# frames: invisible rectangle that you can put things in
top_frame = Frame(window)
top_frame.pack()
bottom_frame = Frame(window)
bottom_frame.pack(side=BOTTOM)

# button = Button(where do you want to put it, text=default value, fg=colour)
button1 = Button(top_frame, text="button1", fg="red")
button2 = Button(top_frame, text="button1", fg="blue")
button3 = Button(top_frame, text="button1", fg="green")
button4 = Button(bottom_frame,  text="button1", fg="purple")

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

window.mainloop()
