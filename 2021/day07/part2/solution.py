from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Parsing input...")
with open(INPUT_PATH, "r") as infile:
    input_numbers: [int] = [int(n) for n in infile.read().strip().split(",")]
LOGGER.tee(f"Successfully read {len(input_numbers)} numbers.")


class CrabSub:
    origin_pos: int
    position: int

    fuel_cost: int
    used_fuel: int

    def __init__(self, position: int):
        self.origin_pos = position
        self.position = position

        self.starting_fuel = 1
        self.used_fuel = 0

    def __str__(self):
        return f"Crab Submarine at {self.position:4}"

    def __repr__(self):
        return f"CrabSub({position})"

    def move_to(self, new_pos: int) -> int:
        diff: int = max(self.position, new_pos) - min(self.position, new_pos)
        return sum(range(1, diff+1))

    def reset(self):
        self.position = self.origin_pos
        self.used_fuel = 0


LOGGER.tee("Creating crab submarines...")
subs: [CrabSub] = []
for inx in tqdm(range(len(input_numbers))):
    input_number: int = input_numbers[inx]
    sub: CrabSub = CrabSub(input_number)
    subs.append(sub)
LOGGER.tee(f"Created {len(subs)} submarines.")
LOGGER.tee()
LOGGER.tee("Finding lowest fuel usage possible...")
lower_bound: int = min(input_numbers)
upper_bound: int = max(input_numbers)
total_costs: int = [0 for _ in range(0, upper_bound+1)]
for pos in tqdm(range(lower_bound, upper_bound+1)):
    fuel_usages: [int] = []
    for sub in subs:
        used_fuel: int = sub.move_to(pos)
        fuel_usages.append(used_fuel)
    full_usage: int = sum(fuel_usages)
    total_costs[pos] = full_usage
    [sub.reset() for sub in subs]
LOGGER.tee(f"Lowest fuel usage is {min(total_costs)} fuel units.")


# Write our logs to the output file
LOGGER.dump_log()
