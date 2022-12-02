from wtslog import Logger
from typing import Union
from tqdm import tqdm

INPUT_PATH: str = "../input"

LETTERMATCH: dict = {
    "A": "r", "X": "r",
    "B": "p", "Y": "p",
    "C": "s", "Z": "s"
}
WINCONDITIONS: dict = { "r": "s", "p": "r", "s": "p" } # K wins against V
SCORES: dict = { "r": 1, "p": 2, "s": 3 }


def wins(_: str, against: str) -> bool:
    a = LETTERMATCH[_]
    b = LETTERMATCH[against]
    
    return WINCONDITIONS[a] == b


def outcomeScore(game: (str, str)) -> int:
    if wins(game[1], game[0]):
        return 6
    elif LETTERMATCH[game[1]] == LETTERMATCH[game[0]]:
        return 3
    else:
        return 0


with open(INPUT_PATH, "r") as inFile:
    games: [(str, str)] = [tuple(line.split(" ")) for line in inFile.read().strip().split("\n")]

ownSignScores = [SCORES[LETTERMATCH[game[1]]] for game in games]
outcomeScores = [outcomeScore(game) for game in games]
print(sum(ownSignScores) + sum(outcomeScores))