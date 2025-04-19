from tkinter import *
from pygame import init, mixer
init()
mixer.music.load('music\\frostbite caves.mp3')
mixer.music.play(-1)

def name():
    print('name')

def register():
    print('regos')

def draw_image(img):
    can.create_image(250, 150, image=img)

def set_title(mess):
    lab.config(text=mess)

class Scene:
    def __init__(self, img: PhotoImage=None, buttons_text: list[str]=None,
                 buttons_commands: list[any]=None, title: str=None):
        self.img = img
        self.buttons_text = buttons_text
        self.buttons_commands = buttons_commands
        self.title = title
    
    def activate(self):
        global img, buttons

        for but, text, comms in zip(buttons, self.buttons_text, self.buttons_commands):
            but.config(text=text, command=comms)

        draw_image(self.img)
        set_title(self.title)

#class Player:
    #def __init__(self, hp: int=10):
        #self.hp = hp
        

# create windo\/
win = Tk()
win.title('game')
win.geometry('500x300')

# scenes \/
settings_activate = lambda: settings.activate()
shop_activate = lambda: shop.activate()

main_menu = Scene(
    PhotoImage(master=win, file='images\\frost1.png'),
    ['settings', 'shop', 'play'],
    [settings_activate, shop_activate, register],
    'main menu'
)
settings = Scene(
    PhotoImage(file='images\\frost1.png'),
    ['music on/off', 'sounds on/off', 'back'],
    [name, name, main_menu.activate],
    'settings'
)
shop = Scene(
    PhotoImage(file='images\\frost1.png'),
    ['sharpen the sword\nprice: 500', 'heal potion\nprice: 50', 'back'],
    [name, name, main_menu.activate],
    'shop'
)


# canvas \/
can = Canvas(win, width=500, height=500)

buttons = [Button(win, text='"empty"', command=name),
           Button(win, text='play!', command=main_menu.activate),
           Button(win, text='"empty"', command=name)]
img = PhotoImage(file='images\\just_lucas.png')
lab = Label(win, text='Welcome!', bg='#7c93bb', fg='white')

can.create_image(250, 150, image=img)

can.create_window(100, (y := 250), width=(w := 100), height=(h := 30), window=buttons[0])
can.create_window(250, y, width=w, height=h, window=buttons[1])
can.create_window(400, y, width=w, height=h, window=buttons[2])

can.create_window(250, 14, width=500, height=25, window=lab)
can.pack()

win.mainloop()