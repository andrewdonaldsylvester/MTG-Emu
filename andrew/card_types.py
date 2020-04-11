import requests


def fetch_card_data(card_name):
    result = requests.get("https://api.scryfall.com/cards/named?exact={}".format(card_name.replace(' ', '+')))
    return result.json()


print(fetch_card_data("Wrenn and Six"))


class Card(object):
    def __init__(self, name):
        self.name = name
        self.card_data = fetch_card_data(self.name)
        self.mana_cost = self.card_data['mana_cost']
        self.image = self.card_data['image_uris']['large']
        self.colors = self.card_data['colors']
        self.color_identity = self.card_data['color_identity']
        try:
            self.color_indicator = self.card_data['color_indicator']
        except:
            self.color_indicator = None
        self.type_line = self.card_data['type_line']
        # self.expansion_symbol = expansion_symbol
        self.text_box = self.card_data['oracle_text']
        # self.extra_info = extra_info


class Creature(Card):
    def __init__(self, name):  # add abilities as a list or maybe just haste; add summoning sickness as a trait
        Card.__init__(self, name)
        self.starting_power = self.card_data['power']
        self.starting_toughness = self.card_data['toughness']
        self.power = self.starting_power
        self.toughness = self.starting_toughness
        self.marked_damage = 0


class Artifact(Card):
    def __init__(self, name):
        Card.__init__(self, name)


class Enchantment(Card):
    def __init__(self, name):
        Card.__init__(self, name)


class Land(Card):
    def __init__(self, name):
        Card.__init__(self, name)


class Planeswalker(Card):
    def __init__(self, name):  # put loyalty abilities as a dictionary with cost:ability
        Card.__init__(self, name)
        self.starting_loyalty = self.card_data['loyalty']
        self.loyalty = self.starting_loyalty
        # self.loyalty_abilities = loyalty_abilities
        # self.static_abilities = static_abilities


class Instant(Card):
    def __init__(self, name):
        Card.__init__(self, name)


class Sorcery(Card):
    def __init__(self, name):
        Card.__init__(self, name)


ramos = Creature('Ramos, Dragon Engine')

print(ramos.image)
