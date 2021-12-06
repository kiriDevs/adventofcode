from __future__ import annotations
from tqdm import tqdm
from typing import Union

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

# Task-specific constants
SIMULATION_DAY_COUNT: int = 80

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)


class Lanternfish:
    timer: int
    def __init__(self, timer):
        self.timer = timer

    @classmethod
    def birth(cls) -> Lanternfish:
        return Lanternfish(8)

    def give_birth(self) -> Lanterfish:
        self.timer = 6
        return Lanternfish.birth()

    def tick(self) -> Union[Lanternfish, None]:
        self.timer -= 1
        if self.timer == -1:
            new_fish: Lanternfish = self.give_birth()
            return new_fish


LOGGER.tee(f"Parsing input...")
with open(INPUT_PATH, "r") as input_file:
    input_numbers: [int] = input_file.read().strip().split(",")
input_numbers = [int(num) for num in input_numbers]
LOGGER.tee(f"Read {len(input_numbers)} input numbers.")
LOGGER.indent()
LOGGER.log(input_numbers)
LOGGER.unindent()

lanternfishes: [Lanternfish] = []

LOGGER.tee()

LOGGER.tee(f"Creating initial fishes...")
for input_inx in tqdm(range(len(input_numbers))):
    input_number: int = input_numbers[input_inx]
    new_lf: Lanternfish = Lanternfish(input_number)
    lanternfishes.append(new_lf)
LOGGER.tee(f"Created {len(lanternfishes)} initial lanternfishes.")

LOGGER.tee()

LOGGER.tee(f"Simulating {SIMULATION_DAY_COUNT} days.")
for day_inx in tqdm(range(SIMULATION_DAY_COUNT)):
    LOGGER.log(f"Simulating day {day_inx:3}...")
    LOGGER.indent()
    new_lanternfishes: [Lanternfish] = []
    for lf_inx in range(len(lanternfishes)):
        LOGGER.indent()
        lf: Lanternfish = lanternfishes[lf_inx]
        new_lf: Lanternfish = lf.tick()
        if new_lf is not None:
            new_lanternfishes.append(new_lf)
        LOGGER.unindent()
    LOGGER.log(f"Comitting {len(new_lanternfishes)} new fishes to main list.")
    lanternfishes += new_lanternfishes
    new_amount: int = len(new_lanternfishes)
    LOGGER.unindent()
    LOGGER.log(f"Finishing day {day_inx:3} with {new_amount} new lanternfishes.")
LOGGER.tee(f"Simulation finished. There are now {len(lanternfishes)} fishes.")

# Write our logs to the output file
LOGGER.dump_log()
