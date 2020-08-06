from tkinter import *
from PIL import Image, ImageTk

# tkinter window
root = Tk()
root.title('Clicker')

# define x and y sizes
size = (400, 400)

# set size of the window
root.geometry('x'.join([str(i) for i in size]))

# create a frame in the window (same size as window)
w = Frame(root, height=size[0], width=size[1])
w.pack()

# keep track of clicks
count = 0

# StringVar to display clicks and messages
displayCount = StringVar()
displayCount.set('Click Me')

click = Label(w, textvariable=displayCount, justify=CENTER, anchor=CENTER)
click.pack()

# open and resize image
im = Image.open("doge.jpg")

# crop square
imgW, imgH = im.size

if imgW < imgH:
    print('cut height')
    im = im.crop((0, (imgH - imgW)//2, imgW, imgH - (imgH - imgW)//2 ))
elif imgW > imgH:
    print('cut width')
    im = im.crop(((imgW - imgH)//2, 0, imgW - (imgW - imgH)//2, imgH))
    
im = im.resize( (size[0]//2, size[1]//2) )
doge = ImageTk.PhotoImage(im)
# create canvas in Frame
canvas = Canvas(w, width=size[0], height=size[1])
canvas.pack()
# create image on canvas
dogeSprite = canvas.create_image(size[0]/2,size[1]/2, image=doge)

def clicked(a):
    global count
    count += 1
    displayCount.set(str(count))


click.bind('<Button-1>', clicked)

mainloop()
