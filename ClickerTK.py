from tkinter import *

# tkinter window
root = Tk()
root.title('Clicker')

size = (400, 400)

root.geometry('x'.join([str(i) for i in size]))

w = Frame(root, height=size[0], width=size[1])
w.pack()

count = 0
displayCount = StringVar()
displayCount.set('Click Me')

click = Label(w, textvariable=displayCount, justify=CENTER, anchor=CENTER)
click.pack()

def clicked(a):
    global count
    count += 1
    displayCount.set(str(count))
    print(count)


click.bind('<Button-1>', clicked)

mainloop()
