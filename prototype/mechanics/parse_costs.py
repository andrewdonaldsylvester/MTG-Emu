import re

costs = [
    "{2}{U}",
    "{B}{G}, Sacrifice another creature",
    "{R}, {T}",
    "{3}{U}",
    "{G/P}",
    "Sacrifice a Swamp and a Forest"

]


def parse_costs(costs):
    cost = []
    # matches = re.search(r"(?:{(.)}+)", costs)
    matches = re.findall(r"{(.*?)}", costs)
    if matches is not None:
        # print(matches.group(0).upper(),matches.group(1).upper())
        next = re.sub(r"{(.*?)}", "", costs)
        print("{:40s} {:40s} {:40s}".format(costs, ",".join(matches), next))

for cost in costs:
    parse_costs(cost)
