from tkinter import *
from PIL import Image, ImageTk

class dog_clicker:
    
    # keep track of clicks
    _count = 0
    _money = 0

    target = 10
    canClick = True
    level = 0
    target = 0
    
    def __init__(self):
        # tkinter window
        self.root = Tk()
        self.root.title('Clicker')

        # define x and y sizes
        self.size = (400, 400)

        # set size of the window
        self.root.geometry('x'.join([str(i) for i in self.size]))

        # create a frame in the window (same size as window)
        self.w = Frame(self.root, height=self.size[0], width=self.size[1])
        self.w.pack()

        # StringVar to display clicks and messages
        self.displayCount = StringVar()

        Label(self.w, textvariable=self.displayCount, justify=CENTER, anchor=CENTER).pack()


        # open and resize image
        self.im = Image.open("doge.png")

        
        # create canvas in Frame
        self.canvas = Canvas(self.w, width=self.size[0], height=self.size[1])
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.clicked)
        self.reset()

        mainloop()

    def create_image(self, level):
        # crop square
        imgW, imgH = self.im.size
        cSizeW, cSizeH = (self.size[0]//2, self.size[1]//2)
        img = self.im.copy()

        if imgW < imgH:
            img = self.im.crop((0, (imgH - imgW)//2, imgW, imgH - (imgH - imgW)//2 ))
        elif imgW > imgH:
            img = self.im.crop(((imgW - imgH)//2, 0, imgW - (imgW - imgH)//2, imgH))
        
        img = img.resize( (cSizeW//level, cSizeH//level) )
        doge = Image.new('RGBA', (cSizeW, cSizeH))
        for i in range(level):
            for j in range(level):
                doge.paste(img, (i*cSizeW//level, j*cSizeH//level))
        self.doge = ImageTk.PhotoImage(doge)
        # create image on canvas
        dogeSprite = self.canvas.create_image(self.size[0]/2,self.size[1]/2, image=self.doge)
        
    def auto_click(self):
        if self.canClick:
            self.inc_count(self.level**2)
            self.w.after(1000, self.auto_click)

    def reset(self):
        self._count = 0
        self.displayCount.set('Click Me!')
        self._money += self.target
        self.level += 1
        self.target = 10 ** self.level
        self.canClick = True
        self.create_image(self.level)
        self.auto_click()

    def clicked(self, a):
        if not self.canClick:
            return
        self.inc_count(1)

    def inc_count(self, inc):
        self._count += inc
        if self._count >= self.target:
            self.canClick = False
            self.displayCount.set('You Win!')
            self.w.after(5000, self.reset)
        else:
            self._money += inc
            print(self._money)
            self.displayCount.set(str(self._count))

class upgrade:
    
    level = 0
    
    def __init__(self):
        pass

    def buy_upgrade(self):
        pass

if __name__ == '__main__':
    d = dog_clicker()
