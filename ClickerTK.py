from tkinter import *
from PIL import Image, ImageTk

class upgrade:
    
    _level = 1
    _cost = 10
    
    def __init__(self, startLevel):
        self._level = startLevel

    def set_string_var(self, stringVar, name):
        self._name = name
        self._displayCost = stringVar
        self.display_cost()

    def get_string_var(self):
        return self._displayCost

    def buy_upgrade(self, stats):
        if stats['money'] > self._cost:
            stats['money'] -= self._cost
            self._level += 1
            self._cost *= 10
            self.display_cost()

    def display_cost(self):
        print(self._name)
        self._displayCost.set(f'{self._name}\nCost: {self.get_cost()}\nLevel: {self.get_level()}')

    def set_level(self, level):
        self._level = level

    def get_level(self):
        return self._level

    def set_cost(self, cost):
        self._cost = cost

    def get_cost(self):
        return self._cost
    
class dog_clicker:
    
    # keep track of clicks
    stats = {
        'count': 0,
        'money': 0
    }

    upgrades = {
        'Points per Click': upgrade(1),
        'Autoclick Speed': upgrade(1)
    }

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

        self.buttons_frame = Frame(self.root)
        self.buttons_frame.pack(side=BOTTOM)

        # StringVar to display clicks and messages
        self.displayCount = StringVar()

        Label(self.root, textvariable=self.displayCount, justify=CENTER, anchor=CENTER).pack()


        # open and resize image
        self.im = Image.open("doge.png")

        
        # create canvas in Frame
        self.canvas = Canvas(self.root, width=self.size[0], height=self.size[1])
        self.canvas.pack(side=TOP)

        # buttons for upgrades
        for each in self.upgrades:
            self.upgrades[each].set_string_var(StringVar(), each)
            Button(
                self.buttons_frame,
                textvariable=self.upgrades[each].get_string_var(),
                command = lambda name=each: self.upgrades[name].buy_upgrade(self.stats)
                ).pack(side=LEFT)
            print(self.upgrades[each]._name)
            

        # bind left click to canvas
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
            # TODO: don't let timer go negative
            self.canvas.after(3000 - ((self.upgrades['Autoclick Speed'].get_level()-1)*1000), self.auto_click)

    def reset(self):
        self.stats['count'] = 0
        self.displayCount.set('Click Me!')
        self.stats['money'] += self.target
        self.level += 1
        self.target = 10 ** self.level
        self.canClick = True
        self.create_image(self.level)
        self.auto_click()

    def clicked(self, a):
        if not self.canClick:
            return
        self.inc_count(self.upgrades['Points per Click'].get_level())

    def inc_count(self, inc):
        self.stats['count'] += inc
        self.stats['money'] += inc
        self.displayCount.set(f"{self.stats['count']}\n{self.stats['money']}")
        if self.stats['count'] >= self.target:
            self.canClick = False
            self.displayCount.set(f"You Win!\n{self.stats['money']}")
            self.canvas.after(5000, self.reset)
       

if __name__ == '__main__':
    d = dog_clicker()
