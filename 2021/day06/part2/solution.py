from __future__ import annotations
from tqdm import tqdm
from typing import Union

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

# Task-specific constants
SIMULATION_DAY_COUNT: int = 256

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee(f"Parsing input...")
with open(INPUT_PATH, "r") as input_file:
    input_numbers: [int] = input_file.read().strip().split(",")
input_numbers = [int(num) for num in input_numbers]
LOGGER.tee(f"Read {len(input_numbers)} input numbers.")
LOGGER.indent()
LOGGER.log(input_numbers)
LOGGER.unindent()

LOGGER.tee()

lanternfishes: [int] = [0 for _ in range(9)]


def tick():
    global lanternfishes
    new_lanternfishes: [int] = [0 for _ in range(len(lanternfishes))]

    # Move lanternfishes over
    # I tried to loop it but messed up and then just copy-pasted the lines rq
    new_lanternfishes[8] = lanternfishes[0]
    new_lanternfishes[7] = lanternfishes[8]
    new_lanternfishes[6] = lanternfishes[7] + lanternfishes[0]
    new_lanternfishes[5] = lanternfishes[6]
    new_lanternfishes[4] = lanternfishes[5]
    new_lanternfishes[3] = lanternfishes[4]
    new_lanternfishes[2] = lanternfishes[3]
    new_lanternfishes[1] = lanternfishes[2]
    new_lanternfishes[0] = lanternfishes[1]

    # Apply changes to global lanternfishes
    lanternfishes = new_lanternfishes


LOGGER.tee(f"Creating initial fishes...")
for input_number in tqdm(input_numbers):
    lanternfishes[input_number] += 1
LOGGER.tee(f"Created {sum(lanternfishes)} initial lanternfishes:")
LOGGER.tee(lanternfishes)

LOGGER.tee()

LOGGER.tee(f"Simulating {SIMULATION_DAY_COUNT} days.")
LOGGER.indent()
for day_inx in tqdm(range(SIMULATION_DAY_COUNT)):
    LOGGER.log(f"Simulating day {day_inx}...")
    LOGGER.indent()
    tick()
    LOGGER.unindent()
    amounts: [str] = [f'{i}:{lanternfishes[i]}' for i in range(9)]
    LOGGER.log(" ".join(amounts))
LOGGER.unindent()
LOGGER.tee(f"Simulation finished. There are now {sum(lanternfishes)} fishes.")

# Write our logs to the output file
LOGGER.dump_log()
