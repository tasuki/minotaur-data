import json
import sys

fname = sys.argv[1]
data = json.load(open(fname))

for game in data:
    print(game["record"])
