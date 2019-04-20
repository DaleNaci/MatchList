import json
import urllib.request
import pprint
import sys

team = sys.argv[1]

urlStructure = "https://api.vexdb.io/v1/get_matches?season=Turning%20Point&sku=RE-VRC-19-7004&team="
response = urllib.request.urlopen(urlStructure + team)
results = json.loads(response.read())["result"]

allMatches = []

enemyMatches = { }

for match in results:
    if match["blue1"] == team or match["blue2"] == team:
        enemyMatches[match["red1"]] = [match["matchnum"]]
        enemyMatches[match["red2"]] = [match["matchnum"]]
    else:
        enemyMatches[match["blue1"]] = [match["matchnum"]]
        enemyMatches[match["blue2"]] = [match["matchnum"]]

for team in enemyMatches:
    enemyResponse = urllib.request.urlopen(urlStructure + team)
    enemyResults = json.loads(enemyResponse.read())["result"]

    ourMatch = enemyMatches[team].pop(0)
    # getting matches
    for enemyMatch in enemyResults:
        if enemyMatch["matchnum"] < ourMatch:
            enemyMatches[team].append(enemyMatch["matchnum"])
        else:
            break

for key, value in enemyMatches.items():
    print(key + " : " + str(value))

for key in enemyMatches:
    for match in enemyMatches[key]:
        if not match in allMatches:
            allMatches.append(match)

allMatches.sort()
print(allMatches)
