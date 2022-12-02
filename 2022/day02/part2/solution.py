from wtslog import Logger
from typing import Union
from tqdm import tqdm

INPUT_PATH: str = "../input"

LETTERMATCH: dict = {
    "A": "r",
    "B": "p",
    "C": "s"
}
WINCONDITIONS: dict = { "r": "s", "p": "r", "s": "p" } # K wins against V
SCORES: dict = { "r": 1, "p": 2, "s": 3, "X": 0, "Y": 3, "Z": 6 }

with open(INPUT_PATH, "r") as inFile:
    games: [(str, str)] = [tuple(line.split(" ")) for line in inFile.read().strip().split("\n")]

totalScore: int = 0
for game in games:
    # Add the score of the outcome
    totalScore += SCORES[game[1]]

    # Detect what sign we need to play
    ourSign: str = ""
    possibilities: str = ["r", "p", "s"]
    
    if game[1] == "Y":  # If we need to draw
        ourSign = LETTERMATCH[game[0]]
    else:
        possibilities.remove(LETTERMATCH[game[0]])
    
    if game[1] == "X":  # If we need to lose
        ourSign = WINCONDITIONS[LETTERMATCH[game[0]]]
    else:
        possibilities.remove(WINCONDITIONS[LETTERMATCH[game[0]]])

    if ourSign == "":
        ourSign = possibilities[0]

    # Add the score of the sign we need to play
    totalScore += SCORES[ourSign]

print(totalScore)

# 12012 < x