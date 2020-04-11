import asyncio
import re

from aiohttp import ClientSession

ALL_CARDS = "https://www.mtgjson.com/files/AllCards.json"
ALL_PRICES = "https://www.mtgjson.com/files/AllPrices.json"
CARD_TYPES = "https://www.mtgjson.com/files/CardTypes.json"
KEY_WORDS = "https://www.mtgjson.com/files/Keywords.json"
SET_LIST = "https://www.mtgjson.com/files/SetList.json"
SLU_SET = "https://www.mtgjson.com/json/SLU.json"
ELD_SET = "https://www.mtgjson.com/json/ELD.json"
M20_SET = "https://www.mtgjson.com/json/M20.json"

keyword_abilities = [
    "Deathtouch",
    "Defender",
    "Double Strike",
    "Enchant",
    "Equip",
    "First Strike",
    "Flash",
    "Flying",
    "Haste",
    "Hexproof",
    "Indestructible",
    "Lifelink",
    "Menace",
    "Prowess",
    "Reach",
    "Trample",
    "Vigilance",
    "Absorb",
    "Affinity",
    "Amplify",
    "Annihilator",
    "Aura Swap",
    "Awaken",
    "Banding",
    "Battle Cry",
    "Bestow",
    "Bloodthirst",
    "Bushido",
    "Buyback",
    "Cascade",
    "Champion",
    "Changeling",
    "Cipher",
    "Conspire",
    "Convoke",
    "Cumulative Upkeep",
    "Cycling",
    "Dash",
    "Delve",
    "Dethrone",
    "Devoid",
    "Devour",
    "Dredge",
    "Echo",
    "Entwine",
    "Epic",
    "Evoke",
    "Evolve",
    "Exalted",
    "Exploit",
    "Extort",
    "Fading",
    "Fear",
    "Flanking",
    "Flashback",
    "Forecast",
    "Fortify",
    "Frenzy",
    "Fuse",
    "Graft",
    "Gravestorm",
    "Haunt",
    "Hidden Agenda",
    "Hideaway",
    "Horsemanship",
    "Infect",
    "Ingest",
    "Intimidate",
    "Kicker",
    "Landhome",
    "Landwalk",
    "Level Up",
    "Living Weapon",
    "Madness",
    "Megamorph",
    "Miracle",
    "Modular",
    "Morph",
    "Myriad",
    "Ninjutsu",
    "Offering",
    "Outlast",
    "Overload",
    "Persist",
    "Phasing",
    "Poisonous",
    "Protection",
    "Provoke",
    "Prowl",
    "Rampage",
    "Rebound",
    "Recover",
    "Reinforce",
    "Renown",
    "Replicate",
    "Retrace",
    "Ripple",
    "Scavenge",
    "Skulk",
    "Shadow",
    "Shroud",
    "Soulbond",
    "Soulshift",
    "Splice",
    "Split Second",
    "Storm",
    "Substance",
    "Sunburst",
    "Surge",
    "Suspend",
    "Totem Armor",
    "Transfigure",
    "Transmute",
    "Tribute",
    "Undying",
    "Unearth",
    "Unleash",
    "Vanishing",
    "Wither",
]


def xstr(s):
    if s is None or s == []:
        return ""
    else:
        return ",".join(s)


def afetch(data_set, url):
    return asyncio.ensure_future(fetch(data_set, url))


async def fetch(data_set, url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
            data[data_set] = response
            print("Got {}".format(url))


def find_activated_ability(line):
    matches = re.search(r"^(\{[a-zA-Z0-9]\}[, ]*)+", line)
    if matches is not None:
        activation = matches.group(0).upper()
        ability = line[len(activation) :]
        if activation is not None:
            return re.sub(r"[, ]", "", activation), re.sub(r"^: ", "", ability)
    return None, None


def find_ability(line):
    found_ability = None
    matches = re.search(r"^\s*[,]*\s*([a-zA-Z]+)", line)
    if matches is None:
        matches = re.search(r"^([a-zA-Z]+ [sS]trike)", line)
    if matches is not None:
        match = matches.group(1).upper()
        if match in map(str.upper, keyword_abilities):
            found_ability = match
        else:
            matches = re.search(r"^([a-zA-Z]+ [sS]trike)", line)
        if matches is not None:
            match = matches.group(1).upper()
            if match in map(str.upper, keyword_abilities):
                found_ability = match
    if found_ability is not None:
        yield found_ability
        for ability in find_ability(line[len(found_ability) :]):
            yield ability


def find_abilities(text):
    found_abilities = []
    for line in text.split("\n"):
        for ability in find_ability(line):
            found_abilities.append(ability)
    return found_abilities


loop = asyncio.get_event_loop()
tasks = []
data = {}
print("Fetching ALL CARDS from {} ...".format(ALL_CARDS))
tasks.append(afetch("all_cards", ALL_CARDS))
# print("Fetching ALL PRICES from {} ...".format(ALL_PRICES))
# tasks.append(afetch("all_prices", ALL_PRICES))
print("Fetching CARD TYPES from {} ...".format(CARD_TYPES))
tasks.append(afetch("card_types", CARD_TYPES))
print("Fetching KEY WORDS from {} ...".format(KEY_WORDS))
tasks.append(fetch("key_words", KEY_WORDS))
print("Fetching SET LIST from {} ...".format(SET_LIST))
tasks.append(fetch("set_list", SET_LIST))
print("Fetching SLU SET from {} ...".format(SLU_SET))
tasks.append(fetch("slu_set", SLU_SET))
print("Fetching ELD SET from {} ...".format(ELD_SET))
tasks.append(fetch("eld_set", ELD_SET))
print("Fetching M20 SET from {} ...".format(M20_SET))
tasks.append(fetch("m20_set", M20_SET))
print("Waiting ...")
loop.run_until_complete(asyncio.wait(tasks))
print("Done!")
print("Wait!")
m20_set = data["m20_set"]
all_cards = data["all_cards"]

print()
print()
print("Keyword Abilities")
i = 1
# for card_name in all_cards:
#     card = all_cards[card_name]
for card in m20_set["cards"]:
    if "Creature" in card["types"]:
        text = card["text"].replace("\n", " \\n ") if "text" in card else ""
        abilities = find_abilities(card["text"] if "text" in card else "")
        ability_string = xstr(abilities)
        print("{:03d} {:30s} {:30s} {}".format(i, card["name"], ability_string, text))
        i += 1

print()
print()
print("Activated abilities.")

i = 1
for card in m20_set["cards"]:
    if "Creature" in card["types"]:
        text = card["text"] if "text" in card else ""
        for line in text.split("\n"):
            activation, ability = find_activated_ability(line)
            if activation is not None:
                print(
                    "{:03d} {:30s} {:20s} {:180s} **** {}".format(
                        i, card["name"], activation, ability, line
                    )
                )
                i += 1
