from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

# Task-specific constants
openers: [str] = ["(", "[", "{", "<"]
closers: [str] = [")", "]", "}", ">"]
pairs: [str] = ["()", "[]", "{}", "<>"]
points_table: dict = { ")": 3, "]": 57, "}": 1197, ">": 25137 }

LOGGER.tee("Loading input...")
with open(INPUT_PATH, "r") as infile:
    inlines: [str] = infile.read().strip().split("\n")
LOGGER.tee(f"Successfully loaded {len(inlines)} lines of input.")

LOGGER.tee()

LOGGER.tee("Parsing input...")
LOGGER.indent()
score: int = 0
for linx, line in tqdm(enumerate(inlines)):
    old: int = score
    LOGGER.log(f"Processing line {linx}")
    LOGGER.indent()
    oldlen: int = len(line)
    LOGGER.log("Removing pairs...")
    while any([a in line for a in pairs]):
        for a in pairs:
            line = line.replace(a, "")
    LOGGER.log(f"Removed {oldlen-len(line):3} characters")
    LOGGER.log(f"Remainder: {line}")
    if not any([a in line for a in closers]):
        LOGGER.log("No closer remains, line is just incomplete.")
    else:
        LOGGER.log("Searching for first incorrect closer...")
        LOGGER.indent()
        positions: [int] = []
        for closer in closers:
            pos: int = line.find(closer)
            if pos == -1:
                LOGGER.log(f"No {closer} was found. Line is just incomplete.")
            else:
                positions.append(pos);
                LOGGER.log(f"{closer} occurs for the first time at i{pos:2}")
        LOGGER.unindent()
        firstclose: str = line[min(positions)]
        score += points_table[firstclose]
        LOGGER.log(f"First bad closer: {firstclose} at {min(positions):2}")
    LOGGER.unindent()
    LOGGER.log(f"Score changed: {old} -> {score}")
LOGGER.unindent()
LOGGER.tee()
LOGGER.tee(f"SOLVE: Your solution is {score}.")

# Write our logs to the output file
LOGGER.dump_log()
