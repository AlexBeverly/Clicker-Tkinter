from tkinter import *
from PIL import Image, ImageTk
import os
import json
# JSON
# JavaScript Object Notation
# stats, upgrade levels

class upgrade:
    
    _level = 1
    _cost = 10
    
    def __init__(self, startLevel):
        self._level = startLevel

    # set stringVar to display cost when changed
    def set_string_var(self, stringVar, name):
        self._name = name
        self._displayCost = stringVar
        self.display_cost()

    def get_string_var(self):
        return self._displayCost

    def buy_upgrade(self, stats):
        # check if player has enough money
        if stats['money'] > self._cost:
            # if they do, take money and increment level
            stats['money'] -= self._cost
            self.set_level(self.get_level() + 1)

    # update stringVar to show new cost
    def display_cost(self):
        self._displayCost.set(f'{self._name}\nCost: {self.get_cost()}\nLevel: {self.get_level()}')

    def set_level(self, level):
        self._level = level
        self.set_cost(10**level)
        self.display_cost()

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
        'money': 0,
        'level': 1
    }

    # keep track of upgrade types
    upgrades = {
        'Points per Click': upgrade(1),
        'Autoclick Speed': upgrade(1)
    }

    # track if player can click
    canClick = True

    # track target score
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
                command = lambda name=each: self.buy_upgrade(name)
                ).pack(side=LEFT)
            

        # bind left click to canvas
        self.canvas.bind('<Button-1>', self.clicked)
        
        self.load_game()

        mainloop()

    def buy_upgrade(self, name):
        self.upgrades[name].buy_upgrade(self.stats)
        self.displayCount.set(f"{self.stats['count']}\n{self.stats['money']}")

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

    # click the dog and repeat after delay
    def auto_click(self):
        if self.canClick:
            self.inc_count(self.upgrades['Points per Click'].get_level() * (self.stats['level']**2))
            delay = 3000 - ((self.upgrades['Autoclick Speed'].get_level()-1)*50)

            self.canvas.after((50, delay)[delay > 0], self.auto_click)

    # reset after score reaches target
    def reset(self):
        # reset score
        self.stats['count'] = 0
        # reward player for hitting target
        self.stats['money'] += self.target
        # increment level
        self.stats['level'] += 1
        self.setup()

        
    def setup(self):
        self.displayCount.set('Click Me!')
        # get new target
        self.target = 10 ** self.stats['level']
        # allow player to click
        self.canClick = True
        # tile new dog picture
        self.create_image(self.stats['level'])
        # restart auto clicking
        self.auto_click()
        # save progress
        self.save_game()
        

    # runs when player clicks the dog
    def clicked(self, a):
        # make sure player can click
        if self.canClick:
            # click based on current 'Points per Click' level
            self.inc_count(self.upgrades['Points per Click'].get_level())

    # increases count and money and updates the label
    def inc_count(self, inc):
        self.stats['count'] += inc
        self.stats['money'] += inc
        self.displayCount.set(f"{self.stats['count']}\n{self.stats['money']}")
        # check if target is hit
        if self.stats['count'] >= self.target:
            self.canClick = False
            self.displayCount.set(f"You Win!\n{self.stats['money']}")
            self.canvas.after(5000, self.reset)

    def save_game(self):
        # dictionary to convert to JSON
        save = dict()

        # save stats
        save['stats'] = dict()
        for stat in self.stats:
            save['stats'][stat] = self.stats[stat]

        # save upgrade levels
        save['upgrades'] = dict()
        for upgrade in self.upgrades:
            save['upgrades'][upgrade] = self.upgrades[upgrade].get_level()

        # dump to .json file
        #save_json = json.dumps(save)
        with open('save_file.json', 'w') as f:
            json.dump(save, f)
            

    def load_game(self):
        filename = './save_file.json'
        if os.path.isfile(filename):
            with open(filename) as f:
                data = json.load(f)
            for stat in data['stats']:
                if stat in self.stats:
                    self.stats[stat] = data['stats'][stat]
            for upgrade in data['upgrades']:
                if upgrade in self.upgrades:
                    self.upgrades[upgrade].set_level(data['upgrades'][upgrade])
        self.setup()
       

if __name__ == '__main__':
    d = dog_clicker()
