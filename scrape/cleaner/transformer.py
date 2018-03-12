import json
import sys
import os
import re

class IgnorableError(RuntimeError):
  pass

from_dir = "../bga-scraper/bga-games/"
to_file = "bga-games.txt"

def toAlpha(num):
  alpha = "abcdefghi"
  return alpha[int(num) - 1]

def toStratsPawn(x, y):
  return toAlpha(x) + str(10 - int(y))

def toStratsWall(x, y, orientation):
  return toAlpha(x) + str(9 - int(y)) + orientation[0]

def getWinner(data, x_id, o_id):
  for details in data:
    try:
      if details["type"] == "gameStateChange":
        if details["args"]["action"] == "stGameEnd":
          result = details["args"]["args"]["result"][0]
          if result["rank"] != 1:
            raise Exception("Winner winner chicken dinner")

          if result["player"] == x_id:
            return "x"
          if result["player"] == o_id:
            return "o"
    except KeyError:
      pass

  return ""


def transform(game_id, json_data):
  players = set(re.findall('"player_name":"([^"]*)"', json_data))
  if len(players) != 2:
    #print(len(players))
    #print(players)
    raise IgnorableError("not 2 players")

  data = json.loads(json_data)
  ddd = data["data"]["data"]

  record = []
  for move in ddd:
    for details in move["data"]:
      if details["type"] in ["playToken", "playWall"]:
        if details["type"] == "playToken":
          strats = toStratsPawn(
            details["args"]["x"],
            details["args"]["y"],
          )

        elif details["type"] == "playWall":
          strats = toStratsWall(
            details["args"]["x"],
            details["args"]["y"],
            details["args"]["orientation"],
          )

        record.append(strats)

        if len(record) == 1:
          x_id = details["args"]["player_id"]
          x_name = details["args"]["player_name"]
        if len(record) == 2:
          o_id = details["args"]["player_id"]
          o_name = details["args"]["player_name"]

  if len(record) < 15:
    raise IgnorableError("too few moves")

  winner = getWinner(ddd[-1]["data"], x_id, o_id)

  return '{"game_id": "%s", "x_id": "%s", "x_name": "%s", "o_id": "%s", "o_name": "%s", "winner": "%s", "record": "%s"}' % (
    game_id,
    x_id, x_name,
    o_id, o_name,
    winner, ";".join(record)
  )


files = ["16339338.js"]
files = os.listdir(from_dir)

to_file = open(to_file, "w")
for fname in files:
  print(fname)
  json_data = open(from_dir + fname).read()

  try:
    transformed = transform(fname.replace(".js", ""), json_data)
    to_file.write(transformed + "\n")
  except IgnorableError as e:
    print(e)
