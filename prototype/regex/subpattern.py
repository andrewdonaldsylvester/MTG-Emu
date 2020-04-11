import re

def find_sub(line):
    matches = re.search(r'(\{[a-zA-Z0-9]\})+', line)
    if matches is not None:
        match = matches.group(0).upper()
        print("Hello {}".format(match))

find_sub("{6}{U}{U}: Monstrosity 4. (If this creature isn't monstrous, put four +1/+1 counters on it and it becomes monstrous.) ")