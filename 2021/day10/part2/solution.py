from tqdm import tqdm
from math import floor

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

# Task-specific constants
openers: [str] = ["(", "[", "{", "<"]
closers: [str] = [")", "]", "}", ">"]
pairs: [str] = ["()", "[]", "{}", "<>"]
points_table: dict = { ")": 1, "]": 2, "}": 3, ">": 4 }

LOGGER.tee("Loading input...")
with open(INPUT_PATH, "r") as infile:
    inlines: [str] = infile.read().strip().split("\n")
LOGGER.tee(f"Successfully loaded {len(inlines)} lines of input.")

LOGGER.tee()

LOGGER.tee("Parsing input...")
LOGGER.indent()
incomplete_trunc_lines: [str] = []
for linx, line in tqdm(enumerate(inlines)):
    LOGGER.log(f"Processing line {linx}")
    LOGGER.indent()
    oldlen: int = len(line)
    LOGGER.log("Removing pairs...")
    while any([a in line for a in pairs]):
        for a in pairs:
            line = line.replace(a, "")
    LOGGER.log(f"Removed {oldlen-len(line):3} characters")
    LOGGER.log(f"Remainder: {line}")
    LOGGER.unindent()
    if not any([a in line for a in closers]):
        LOGGER.log("No closer remains -> line incomplete.")
        incomplete_trunc_lines.append(line)
    else:
        LOGGER.log("Remaining has a closer -> corrupted -> discarding...")
LOGGER.unindent()
LOGGER.tee(f"There are {len(incomplete_trunc_lines)} incomplete lines remaining.")

LOGGER.tee()

LOGGER.tee(f"Auto-Completing {len(incomplete_trunc_lines)} lines...")
LOGGER.indent()
completions: [str] = []
for linx, line in tqdm(enumerate(incomplete_trunc_lines)):
    LOGGER.log(f"Completing line {linx}")
    LOGGER.indent()
    chars: [str] = list(line)
    chars.reverse()
    completion_parts: [str] = []
    for char in chars:
        closer: str = closers[openers.index(char)]
        LOGGER.log(f"{char} is matched by {closer}")
        completion_parts.append(closer)
    completion: str = "".join(completion_parts)
    completions.append(completion)
    LOGGER.unindent()
    LOGGER.log(f"Completion: {completion}")
LOGGER.unindent()
LOGGER.tee(f"Produced {len(completions)} completions.")

LOGGER.tee()

LOGGER.tee(f"Scoring {len(completions)} lines")
LOGGER.indent()
scores: [int] = []
for cinx, completion in tqdm(enumerate(completions)):
    LOGGER.log(f"Scoring line {cinx}...")
    LOGGER.indent()
    #completion.reverse()  # Because we start calculating from the back
    LOGGER.log(completion)
    score: int = 0
    for char in list(completion):
        old: int = score
        score *= 5
        score += points_table[char]
        LOGGER.log(f"{char}: {old} -> {score} (diff={points_table[char]})")
    scores.append(score)
    LOGGER.unindent()
    LOGGER.log(f"Line {cinx} has a score of {score}")
LOGGER.unindent()
LOGGER.tee(f"Successfully scored {len(scores)} lines")

LOGGER.tee()

LOGGER.tee("Determining solution...")
solution_candidates: [int] = scores
solution_candidates.sort()
solution_index: int = floor(len(solution_candidates)/2)  # Get the middle index
SOLUTION: int = solution_candidates[solution_index]
LOGGER.tee(f"SOLVE: Your solution is {SOLUTION}!")

# Write our logs to the output file
LOGGER.dump_log()
