import requests
import json

import bs4

welcome_text = """
Welcome to the match list generator!
This program is used to scout qualification matches by listing every
match your opponents have leading up to your match with them.
"""

print(welcome_text)

team = input("Team: ")
event_code = input("Event Code: ")

print()

try:
    res = requests.get("https://www.robotevents.com/robot-competitions/vex-robotics-competition/" + event_code + ".html")
    res.raise_for_status()
except:
    print("Event code does not exist!")
    print()
    exit()

soup = bs4.BeautifulSoup(res.text, "html.parser")
results = soup.select("results")


# Styling string to match dictionary
infoString = results[0].attrs["data"][1:-1]
info_replacements = [
    ("&quot;&quot;", " "),
    ("&quot;", ""),
    ("& ,", ","),
    (", ", ","),
    (",", "\n"),
    (":", ": ")
]
for r in info_replacements:
    infoString = infoString.replace(r[0], r[1])


infoLst = infoString.split("}\n{")

# Deletes extra brackets
infoLst[0] = infoLst[0][1:]
infoLst[-1] = infoLst[-1][:-1]

match_list = []

for s in infoLst:
    res = json.loads("{" + s.replace("\n", ", ") + "}")

    useful_keys = ["matchnum", "red1", "red2", "blue1", "blue2"]
    d = {}
    for k in useful_keys:
        d[k] = res[k]

    match_list.append(d)


# deletes canceled matches
for d in match_list:
    if d["matchnum"] == 1:
        idx = match_list.index(d)
        match_list = match_list[idx:]
        break


# deletes elim matches
elim_matches = []
for d in match_list:
    if d["matchnum"]==1 and match_list.index(d)!=0:
        elim_matches.append(d)

for d in elim_matches:
    match_list.remove(d)


enemyMatches = {}

for match in match_list:
    if match["blue1"] == team or match["blue2"] == team:
        enemyMatches[match["red1"]] = match["matchnum"]
        enemyMatches[match["red2"]] = match["matchnum"]
    elif match["red1"] == team or match["red2"] == team:
        enemyMatches[match["blue1"]] = match["matchnum"]
        enemyMatches[match["blue2"]] = match["matchnum"]


matches = {e:[] for e in enemyMatches}

for d in match_list:
    teams = [
        d["red1"],
        d["red2"],
        d["blue1"],
        d["blue2"]
    ]

    for enemy in enemyMatches:
        if enemy in teams:
            matches[enemy].append(d["matchnum"])


for k, v in matches.items():
    max = enemyMatches[k]
    matches[k] = [i for i in v if i<max]



team_names = {int(k[:-1]): k[-1] for k in matches.keys()}
ordered_teams = [str(n)+team_names[n] for n in sorted(team_names)]

for k in ordered_teams:
    print(k, end="\t")
    lst = matches[k]
    if lst == []:
        print("None")
    else:
        print(" ".join(map(str, lst)))


print()


reversed = {}
for enemy, lst in matches.items():
    for match in lst:
        if match in reversed:
            reversed[match].append(enemy)
        else:
            reversed[match] = [enemy]


for k in sorted(reversed.keys()):
    print(k, end="\t")
    print(" ".join(map(str, reversed[k])))

print()
