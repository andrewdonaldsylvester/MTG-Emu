import aiohttp
import asyncio
import async_timeout
from aiohttp import ClientSession
import re

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
]


def xstr(s):
    if s is None or s == []:
        return ""
    else:
        return " ".join(s)


def afetch(data_set, url):
    return asyncio.ensure_future(fetch(data_set, url))


async def fetch(data_set, url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
            data[data_set] = response
            print("Got {}".format(url))


def find_ability(line):
    found_abilities = []
    found_ability = None
    matches = re.search(r"^\s*[,]*\s*([a-zA-Z]+)", line)
    if matches is None:
        match = re.search(r"^([a-zA-Z]+ [sS]trike)", line)
    if matches is not None:
        match = matches.group(1).upper()
        if match in map(str.upper, keyword_abilities):
            found_ability = match
    found_abilities.append(found_ability)
    if found_ability is not None:
        found_ability = find_ability(line[len(found_ability) :])

    return found_abilities


def find_abilities(text):
    found_abilities = []
    for line in text.split("\n"):
        abilities = find_ability(line)
        found_abilities.append(abilities)
    return found_abilities


loop = asyncio.get_event_loop()
tasks = []
data = {}
# print("Fetching ALL CARDS from {} ...".format(ALL_CARDS))
# tasks.append(afetch("all_cards", ALL_CARDS))
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
i = 1
for card in m20_set["cards"]:
    if "Creature" in card["types"]:
        # print(
        #     "#{:03d} {:40s} Type: {:40s} Types: {:40s} Text: {}".format(
        #         i,
        #         card["name"],
        #         card["type"],
        #         str(card["types"]),
        #         card["text"].replace(" \n ", "") if "text" in card else "",
        #     )
        # )
        # print(card["text"] if "text" in card else "")
        text = card["text"].replace("\n", " \\n ") if "text" in card else ""
        abilities = find_abilities(card["text"] if "text" in card else "")
        ability_string = xstr(abilities)
        print("{:30s} {:30s} Text: {}".format(card["name"], ability_string, text))

    i += 1

#
# for card in m20_set["cards"]:
#     if "Creature" in card["types"]:
#         if "text" in card:
#             # print(card["text"].replace("\n", " \\n "))
#             abilities = parse_abilities(card["text"])
#             print(
#                 "{:30s} {:40s} Text: {}".format(card["name"], abilities, card["text"],)
#             )
