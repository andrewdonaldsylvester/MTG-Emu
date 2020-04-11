import requests


def fetch_card_data(card_name):
    result = requests.get("https://api.scryfall.com/cards/named?exact={}".format(card_name.replace(' ', '+')))
    return result.json()


def find_triggered_abilities(card_name):
    """
    returns a dictionary with the keys being the trigger clause and the values being the effect.
    """
    card_text = fetch_card_data(card_name)['oracle_text'].replace(card_name, 'CARDNAME')
    card_abilities = card_text.split('\n')
    triggered_abilities = {}
    for ability in card_abilities:
        if ability.split(' ')[0] in ['When', 'Whenever', 'At']:
            split_ability = ability.split(',', 1)
            triggered_abilities[split_ability[0]] = split_ability[1]
    return triggered_abilities


def find_activated_abilities(card_name):
    card_text = fetch_card_data(card_name)['oracle_text'].replace(card_name, 'CARDNAME')
    card_abilities = card_text.split('\n')
    activated_abilities = {}
    for ability in card_abilities:
        if ':' in ability:
            split_ability = ability.split(':', 1)
            activated_abilities[split_ability[0]] = split_ability[1]
    return activated_abilities


print(find_triggered_abilities('Hanged Executioner'))
print(find_activated_abilities('Hanged Executioner'))

print(find_triggered_abilities('Manifold Key'))
print(find_activated_abilities('Manifold Key'))
