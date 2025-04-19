from tkinter import *
from pygame import init, mixer
from time import sleep
from random import randint, random, randrange
from threading import Thread

init()
mixer.music.load('music\\frostbite caves.mp3')
mixer.music.play(-1)
no_mp3 = mixer.Sound('music\\no.mp3')
crush = mixer.Sound('music\\crush.mp3')
sword = mixer.Sound('music\\sword.mp3')

play_music = True
play_sounds = True

def name():
    print('name')

def register():
    print('regos')

def draw_image(img):
    can.create_image(250, 150, image=img)

def set_title(mess):
    lab.config(text=mess)

def music_play():
    global play_music
    
    if play_music:
        mixer.music.stop()
        play_music = False
    else:
        mixer.music.play(-1)
        play_music = True
    
def sound_play():
    global play_sounds
    play_sounds = not play_sounds

    if play_sounds:
        no_mp3.play()

def game_over():
    set_title('game over!')
        
# scene\/
class Scene:
    def __init__(self, img: PhotoImage=None, buttons_text: list[str]=None,
                 buttons_commands: list[any]=None, title: str=None):
        self.img = img
        self.buttons_text = buttons_text
        self.buttons_commands = buttons_commands
        self.title = title
    
    def activate(self, upd=None):
        global img, buttons

        for but, text, comms in zip(buttons, self.buttons_text, self.buttons_commands):
            but.config(text=text, command=comms)

        draw_image(self.img)
        set_title(self.title)

        if upd is not None:
            self.update_title(upd)
    
    def update_title(self, text):
        self.title = text
        set_title(self.title)

class Level:
    def __init__(self, enemy, lv_count=0, enemy_power=0):
        self.enemy = enemy
        self.lv_count = lv_count
        self.enemy_power = enemy_power
    
    def fight(self):
        self.lv_count += 1
        fight_side.activate()

        def update_fight_data():
            while pl.hp > 0 and entity.hp > 0:
                upd = lambda: fight_side.update_title(f'level: {self.lv_count}, hp: {pl.hp}, '
                    f'damage: {pl.damage}, enemy hp: {entity.hp}, '
                    f'potions: {pl.potions}')
                upd()
            else:
                upd()
                print('upd: stop!')

        def enemy_attack():
            global entity
            print(self.lv_count)

            sleep(2)
            while pl.hp > 0 and entity.hp > 0:
                entity.attack(pl)
                sleep(3)
            else:
                pl.block = False
                pl.balance += 250

                if pl.hp > 0: 
                    choice.activate()
                    choice.update_title(f'level: {self.lv_count}, hp: {pl.hp}, damage: {pl.damage}, '
                    f'potions: {pl.potions}, balance: {pl.balance}')
                else:
                    game_over()

                entity = Entity(randrange(20, 31, 2), randint(1, 3))
                entity.hp *= self.lv_count
                entity.damage *= self.lv_count
                
                print('fight: stop!')

        Thread(target=enemy_attack).start()
        Thread(target=update_fight_data).start()

# Entity classes\/
class Entity:
    def __init__(self, hp: int, damage: int):
        self.hp = hp
        self.damage = damage
        self.block = False

    def defend(self):
        self.block = True
    
    def attack(self, other):
        if not (oth := other.block) and not (slf := self.block):
            other.hp -= self.damage
            if play_sounds:
                sword.play()
        elif oth:
            other.block = False
            if play_sounds:
                crush.play()
        elif slf and play_sounds:
            no_mp3.play()

    def __gt__(self, other):
        self.attack(other)

class Player(Entity):
    def __init__(self, hp: int, damage: int, balance: int, potions: int):
        super().__init__(hp, damage)
        self.balance = balance
        self.potions = potions
    
    def buy_potion(self):
        if self.balance >= potion_price:
            self.potions += 1
            self.balance -= potion_price
        elif play_sounds:
            no_mp3.play()
        
        shop.update_title(f'balance: {self.balance}, potions: {self.potions}, sword sharpness: {self.damage}')
    
    def sharp(self):
        if self.balance >= sharpen_price:
            self.damage += 2
            self.balance -= sharpen_price
        elif play_sounds:
            no_mp3.play()

        shop.update_title(f'balance: {self.balance}, potions: {self.potions}, sword sharpness: {self.damage}')
    
    def heal(self):
        if self.potions > 0:
            self.potions -= 1
            self.hp += 3
        elif play_sounds:
            no_mp3.play()
        
        choice.update_title(f'level: {lv.lv_count}, hp: {pl.hp}, damage: {pl.damage}, '
        f'potions: {pl.potions}, balance: {pl.balance}')

# create window \/ ===========================
win = Tk()
win.title('game')
win.geometry('500x300')

# entities \/
pl = Player(12, 2, 200, 0)
entity = Entity(randrange(20, 31, 2), randint(1, 3))
lv = Level(entity)

# scenes \/
settings_activate = lambda: settings.activate()
shop_activate = lambda: shop.activate(f'balance: {pl.balance}, potions: {pl.potions}, sword sharpness: {pl.damage}')

main_menu = Scene(
    PhotoImage(master=win, file='images\\frost1.png'),
    ['settings', 'shop', 'play'],
    [settings_activate, shop_activate, lv.fight],
    'main menu'
)
settings = Scene(
    PhotoImage(file='images\\frost1.png'),
    ['music on/off', 'sounds on/off', 'back'],
    [music_play, sound_play, main_menu.activate],
    'settings'
)
shop = Scene(
    PhotoImage(file='images\\frost1.png'),
    [f'sharpen the sword\nprice: {(sharpen_price := 500)}', f'heal potion\nprice: {(potion_price := 50)}', 'back'],
    [pl.sharp, pl.buy_potion, main_menu.activate],
    f'balance: {pl.balance}, potions: {pl.potions}, sword sharpness: {pl.damage}'
)
fight_side = Scene(
    PhotoImage(file='images\\fight side.png'),
    ['attack', 'heal', 'defend'],
    [lambda: pl.attack(entity), pl.heal, pl.defend],
    f'hp: {pl.hp}, damage: {pl.damage}, enemy hp: {entity.hp}, potions: {pl.potions}'
)
choice = Scene(
    PhotoImage(file='images\\fight side peaseful.png'),
    ['next enemy', 'heal', 'main menu'],
    [lv.fight, pl.heal, main_menu.activate],
    f'hp: {pl.hp}, damage: {pl.damage}, potions: {pl.potions}'
)

# canvas \/
can = Canvas(win, width=500, height=500)

buttons = [Button(win, text='empty', command=name),
           Button(win, text='play!', command=main_menu.activate),
           Button(win, text='empty', command=name)]
img = PhotoImage(file='images\\just_lucas.png')
lab = Label(win, text='Welcome!', bg='#7c93bb', fg='white')

can.create_image(250, 150, image=img)

can.create_window(100, (y := 250), width=(w := 100), height=(h := 30), window=buttons[0])
can.create_window(250, y, width=w, height=h, window=buttons[1])
can.create_window(400, y, width=w, height=h, window=buttons[2])

can.create_window(250, 14, width=500, height=25, window=lab)
can.pack()

win.mainloop()