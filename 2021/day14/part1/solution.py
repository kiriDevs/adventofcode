from tqdm import tqdm
from wtslog import Logger

# Setup constants
INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"
SIM_COUNT: int = 10

# Setup logger
LOGGER: Logger = Logger(OUTPUT_PATH)

# Read input
LOGGER.tee("Processing input...")
LOGGER.indent()

with open(INPUT_PATH, "r") as infile:
    inlines: [str] = [a.strip() for a in infile.read().strip().split("\n")]
initial: str = inlines[0]
rules: dict[str, str] = dict([inrule.split(" -> ") for inrule in inlines[2:]])
[LOGGER.log(f"{a} -> {rules[a]}") for a in rules]

LOGGER.unindent()
LOGGER.tee(f"Read {len(rules)} rules. Initial: {initial} ({len(initial)})\n")

LOGGER.tee("Starting simulation...")
LOGGER.indent()

current: str = initial
for i in tqdm(range(SIM_COUNT)):
    LOGGER.log(f"Simulating step {(i+1):0>2} / {SIM_COUNT} | from: {current}")
    LOGGER.indent()
    new: [str] = [current[0]]
    for j in range(len(current) - 1):
        cur_a: str = current[j]
        cur_b: str = current[j + 1]
        cur_pair: str = cur_a + cur_b
        # new.append(cur_a) # This [A] = the last [B]
        if cur_pair in rules:
            new_token: str = rules[cur_pair]
            new.append(new_token)
            LOGGER.log(f"{cur_pair} -> {cur_a}{new_token}{cur_b}")
        else:
            LOGGER.log(f"No rule applies to {cur_pair}")
        new.append(cur_b)
    LOGGER.unindent()
    current = "".join(new)
    LOGGER.log(f"Finished step {(i+1):0>2} / {SIM_COUNT} | result: {current}")

LOGGER.unindent()
LOGGER.tee(f"Simulated {SIM_COUNT} growth steps.\n")
final: str = current

# Count output values
occurences: dict[str, int] = {}
for char in final:
    occurences[char] = occurences.get(char, 0) + 1
max_str: str = max(occurences, key=occurences.get)
min_str: str = min(occurences, key=occurences.get)
max_cnt: int = occurences[max_str]
min_cnt: int = occurences[min_str]
LOGGER.log(occurences)
LOGGER.tee(f" Most occurences: {max_str} (x{max_cnt})")
LOGGER.tee(f"Least occurences: {min_str} (x{min_cnt})")
LOGGER.tee(f"=> SOLUTION: {max_cnt - min_cnt}")

# Dump log output
LOGGER.dump_log()
