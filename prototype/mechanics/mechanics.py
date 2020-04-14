import asyncio
import re
from collections import Counter

from aiohttp import ClientSession

ALL_CARDS = "https://www.mtgjson.com/files/AllCards.json"
ALL_PRICES = "https://www.mtgjson.com/files/AllPrices.json"
CARD_TYPES = "https://www.mtgjson.com/files/CardTypes.json"
KEY_WORDS = "https://www.mtgjson.com/files/Keywords.json"
SET_LIST = "https://www.mtgjson.com/files/SetList.json"
SLU_SET = "https://www.mtgjson.com/json/SLU.json"
ELD_SET = "https://www.mtgjson.com/json/ELD.json"
M20_SET = "https://www.mtgjson.com/json/M20.json"


abilities_count = Counter()

#
# Magic the Gathering Comprehensive Rules
# https://media.wizards.com/images/magic/tcg/resources/rules/MagicCompRules_21031101.pdf
#
# 112.3. There are four general categories of abilities:
#
#   112.3a ** Spell abilities ** are abilities that are followed as instructions while an instant or sorcery spell is
#   resolving. Any text on an instant or sorcery spell is a spell ability unless it’s an activated ability, a triggered
#   ability, or a static ability that fits the criteria described in rule 112.6.
#
#   112.3b ** Activated abilities ** have a cost and an effect. They are written as
#   “[Cost]: [Effect.] [Activation instructions (if any).]” A player may activate such an ability whenever he or she
#   has priority. Doing so puts it on the stack, where it remains until it’s countered, it resolves, or it otherwise
#   leaves the stack. See rule 602, “Activating Activated Abilities.”
#
#   112.3c ** Triggered abilities  **have a trigger condition and an effect. They are written as
#   “[Trigger condition], [effect],” and include (and usually begin with) the word “when,” “whenever,” or “at.”
#   Whenever the trigger event occurs, the ability is put on the stack the next time a player would receive priority
#   and stays there until it’s countered, it resolves, or it otherwise leaves the stack.
#   See rule 603, “Handling Triggered Abilities.”
#
#   112.3d ** Static abilities ** are written as statements. They’re simply true. Static abilities create continuous
#   effects which are active while the permanent with the ability is on the battlefield and has the ability, or while
#   the object with the ability is in the appropriate zone. See rule 604, “Handling Static Abilities.”
#

# List of MTG Keywords
# https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_keywords
#
#


qualifiers = [
    "until end of turn",
    "under your control",
    "creatures you control",
    "permanent you control" "Activate this ability only once each turn",
]

add_abilitiy = [
    "gains",
    "gain",
    "get",
    "gets",
    "enters the battlefield",
    "When",
    "add"
    "Put a +1/+1 counter on another target creature with flying"
    "gets +X/+X until end of turn",
    "gets +1/-1 until end of turn",
    "gets +1/+0 until end of turn",
    "Creatures you control get +1/+0 and gain haste until end of turn",
    "Protection from red",
    "gain control of target permanent",
    "If you would gain life, you gain that much life plus 1 instead",
    "Protection from black",
    "Protection from blue",
    "Protection from green",
    "Protection from white",
    "Protection from red",
]

actions = [
    "Search your library",
    "You may reveal a creature card from among them and put it into your hand",
    "gain control of target permanent",
    "Other creatures you control have trample",
]
additional_costs = [
    "Sacrifice",
    "Draw a card",
    "Sacrifice an artifact or land",
    "Sacrifice a land",
]

# MTG JSON
evergreen_keyword_abilities = [
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
    "Vigilance"]

additional_keyword_abilities = [
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


# keyword_abilities = [
#     "Absorb",
#     "Affinity",
#     "Amplify",
#     "Annihilator",
#     "Aura Swap",
#     "Awaken",
#     "Banding",
#     "Battle Cry",
#     "Bestow",
#     "Bloodthirst",
#     "Bushido",
#     "Buyback",
#     "Cascade",
#     "Champion",
#     "Changeling",
#     "Cipher",
#     "Conspire",
#     "Convoke",
#     "Cumulative Upkeep",
#     "Cycling",
#     "Dash",
#     "Deathtouch",
#     "Defender",
#     "Delve",
#     "Dethrone",
#     "Devoid",
#     "Devour",
#     "Double Strike",
#     "Dredge",
#     "Echo",
#     "Enchant",
#     "Entwine",
#     "Epic",
#     "Equip",
#     "Evoke",
#     "Evolve",
#     "Exalted",
#     "Exploit",
#     "Extort",
#     "Fading",
#     "Fear",
#     "First Strike",
#     "Flanking",
#     "Flash",
#     "Flashback",
#     "Flying",
#     "Forecast",
#     "Fortify",
#     "Frenzy",
#     "Fuse",
#     "Graft",
#     "Gravestorm",
#     "Haste",
#     "Haunt",
#     "Hexproof",
#     "Hidden Agenda",
#     "Hideaway",
#     "Horsemanship",
#     "Indestructible",
#     "Infect",
#     "Ingest",
#     "Intimidate",
#     "Kicker",
#     "Landhome",
#     "Landwalk",
#     "Level Up",
#     "Lifelink",
#     "Living Weapon",
#     "Madness",
#     "Megamorph",
#     "Menace",
#     "Miracle",
#     "Modular",
#     "Morph",
#     "Myriad",
#     "Ninjutsu",
#     "Offering",
#     "Outlast",
#     "Overload",
#     "Persist",
#     "Phasing",
#     "Poisonous",
#     "Protection",
#     "Provoke",
#     "Prowess",
#     "Prowl",
#     "Rampage",
#     "Reach",
#     "Rebound",
#     "Recover",
#     "Reinforce",
#     "Renown",
#     "Replicate",
#     "Retrace",
#     "Ripple",
#     "Scavenge",
#     "Shadow",
#     "Shroud",
#     "Skulk",
#     "Soulbond",
#     "Soulshift",
#     "Splice",
#     "Split Second",
#     "Storm",
#     "Substance",
#     "Sunburst",
#     "Surge",
#     "Suspend",
#     "Totem Armor",
#     "Trample",
#     "Transfigure",
#     "Transmute",
#     "Tribute",
#     "Undying",
#     "Unearth",
#     "Unleash",
#     "Vanishing",
#     "Vigilance",
#     "Wither",
#     "Kicker",
#     "Landhome",
#     "Landwalk",
#     "Level Up",
#     "Lifelink",
#     "Living Weapon",
#     "Madness",
#     "Megamorph",
#     "Menace",
#     "Miracle",
#     "Modular",
#     "Morph",
#     "Myriad",
#     "Ninjutsu",
#     "Offering",
#     "Outlast",
#     "Overload",
#     "Persist",
#     "Phasing",
#     "Poisonous",
#     "Protection",
#     "Provoke",
#     "Prowess",
#     "Prowl",
#     "Rampage",
#     "Reach",
#     "Rebound",
#     "Recover",
#     "Reinforce",
#     "Renown",
#     "Replicate",
#     "Retrace",
#     "Ripple",
#     "Scavenge",
#     "Shadow",
#     "Shroud",
#     "Skulk",
#     "Soulbond",
#     "Soulshift",
#     "Splice",
#     "Split Second",
#     "Storm",
#     "Substance",
#     "Sunburst",
#     "Surge",
#     "Suspend",
#     "Totem Armor",
#     "Trample",
#     "Transfigure",
#     "Transmute",
#     "Tribute",
#     "Undying",
#     "Unearth",
#     "Unleash",
#     "Vanishing",
#     "Vigilance",
#     "Wither",
# ]


keyword_abilities = [
    "Absorb",
    "Affinity",
    "Afflict",
    "Afterlife",
    "Aftermath",
    "Amplify",
    "Annihilator",
    "Ascend",
    "Assist",
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
    "Crew",
    "Cumulative Upkeep",
    "Cycling",
    "Dash",
    "Deathtouch",
    "Defender",
    "Delve",
    "Dethrone",
    "Devoid",
    "Devour",
    "Double Strike",
    "Dredge",
    "Echo",
    "Embalm",
    "Emerge",
    "Enchant",
    "Entwine",
    "Epic",
    "Equip",
    "Escalate",
    "Escape",
    "Eternalize",
    "Evoke",
    "Evolve",
    "Exalted",
    "Exploit",
    "Extort",
    "Fabricate",
    "Fading",
    "Fear",
    "First Strike",
    "Flanking",
    "Flash",
    "Flashback",
    "Flying",
    "Forecast",
    "Fortify",
    "Frenzy",
    "Fuse",
    "Graft",
    "Gravestorm",
    "Haste",
    "Haunt",
    "Hexproof",
    "Hidden Agenda",
    "Hideaway",
    "Horsemanship",
    "Improvise",
    "Indestructible",
    "Infect",
    "Ingest",
    "Intimidate",
    "Jump-Start",
    "Kicker",
    "Landwalk",
    "Level Up",
    "Lifelink",
    "Living Weapon",
    "Madness",
    "Melee",
    "Menace",
    "Mentor",
    "Miracle",
    "Modular",
    "Morph",
    "Myriad",
    "Ninjutsu",
    "Offering",
    "Outlast",
    "Overload",
    "Partner",
    "Persist",
    "Phasing",
    "Poisonous",
    "Protection",
    "Provoke",
    "Prowess",
    "Prowl",
    "Rampage",
    "Reach",
    "Rebound",
    "Recover",
    "Reinforce",
    "Renown",
    "Replicate",
    "Retrace",
    "Riot",
    "Ripple",
    "Scavenge",
    "Shadow",
    "Shroud",
    "Skulk",
    "Soulbond",
    "Soulshift",
    "Spectacle",
    "Splice",
    "Split Second",
    "Storm",
    "Sunburst",
    "Surge",
    "Suspend",
    "Totem Armor",
    "Trample",
    "Transfigure",
    "Transmute",
    "Tribute",
    "Undaunted",
    "Undying",
    "Unearth",
    "Unleash",
    "Vanishing",
    "Vigilance",
    "Wither",
]



keyword_actions = [
    ""
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
    matches = re.search(r"^(.*):(.*)", line)
    if matches is not None:
        cost = matches.group(1)
        effect = matches.group(2)
        if cost is not None:
            return cost, effect
    return None, None

# def find_activated_ability(line):
#     matches = re.search(r"^(\{[a-zA-Z0-9]\}[, ]*)+", line)
#     if matches is not None:
#         activation = matches.group(0).upper()
#         ability = line[len(activation) :]
#         if activation is not None:
#             return re.sub(r"[, ]", "", activation), re.sub(r"^: ", "", ability)
#     return None, None


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
        abilities_count[found_ability] += 1
        yield found_ability
        for ability in find_ability(line[len(found_ability) :]):
            abilities_count[found_ability] += 1
            yield ability


def find_abilities(text):
    found_abilities = []
    for line in text.split("\n"):
        for ability in find_ability(line):
            found_abilities.append(ability)
    return found_abilities


def parse_costs(costs):
    cost = []
    # matches = re.search(r"(?:{(.)}+)", costs)
    matches = re.findall(r"{(.*?)}", costs)
    if matches is not None:
        # print(matches.group(0).upper(),matches.group(1).upper())
        next = re.sub(r"{(.*?)}", "", costs)
        print("{:40s} {:40s} {:40s}".format(costs, ",".join(matches), next))
        costs = matches
    if len(next) !=0:
        additional_cost = re.sub(r"^.*, ","", next)
        if len(additional_cost) != 0:
            costs.append(additional_cost)
    return costs


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
for card_name in all_cards:
    card = all_cards[card_name]
# for card in m20_set["cards"]:
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
cost_count = Counter()
# for card in m20_set["cards"]:
for card_name in all_cards:
    card = all_cards[card_name]
    if "Creature" in card["types"]:
        text = card["text"] if "text" in card else ""
        for line in text.split("\n"):
            cost, effect = find_activated_ability(line)
            if cost is not None:
                costs = parse_costs(cost)
                for c in costs:
                    cost_count[c] += 1
                if c is not None:
                    print(
                        "{:03d}; {:30s}; {:80s}; {:180s}; ****; {}".format(
                            i, card["name"], c, effect, line
                        )
                    )
                    i += 1
print("\n\n\n\n")
i = 1
print("Most common keyword abilities:")
for count in abilities_count.most_common(200):
    print("#{:3d} {:20s}: {:5,d}".format(i, count[0], count[1]))
    i+=1

i = 1
print("Most common costs for Activated Abilities:")
for count in cost_count.most_common(2000):
    print("#{:4d}  {:5,d}: {:60s}".format(i, count[1], count[0]))
    i+=1