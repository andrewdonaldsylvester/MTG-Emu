import requests
from tkinter import *
from PIL import ImageTk,Image
import shutil


def get_image(name):
    image_url = fetch_card_data(name)['image_uris']['normal']
    resp = requests.get(image_url, stream=True)
    local_file = open('{}.jpg'.format(name.replace(' ', '_')), 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp


def fetch_card_data(card_name):
    result = requests.get("https://api.scryfall.com/cards/named?exact={}".format(card_name.replace(' ', '+')))
    return result.json()


class Card(object):
    def __init__(self, name):
        self.name = name
        get_image(self.name)
        self.image = '{}.jpg'.format(self.name.replace(' ', '_'))
        self.zone = None
        self.tapped = False


class Deck(object):
    def __init__(self, decklist):
        self.decklist = decklist
        self.cards = []
        for card_name in decklist:
            self.cards.append(Card(card_name))


my_deck = Deck(['Mountain', 'Goblin Guide'])

master = Tk()

canvas = Canvas(master, width=3440, height=1440)


x_cord = 0
for card in my_deck.cards:
    img = ImageTk.PhotoImage(Image.open(card.image))
    canvas.create_image(x_cord, 20, anchor=NW, image=img)
    x_cord += 488

canvas.pack()

mainloop()

