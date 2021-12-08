from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

# Task-specific constants
uniqueSegmentAmounts: dict = { 2:1, 4:4, 3:7, 7:8 }  # len(segs) : value

LOGGER.tee("Loading input data...")
with open(INPUT_PATH, "r") as infile:
    input_lines: [str] = [a.strip() for a in infile.read().strip().split("\n")]
    input_data: [[str]] = [b.split(" | ") for b in input_lines]
inlc: int = len(input_lines)
indc: int = len(input_data)
LOGGER.tee(f"Successfully read {indc} data points from {inlc} input lines.")
del inlc, indc

LOGGER.tee()

LOGGER.tee("Parsing input...")
simple_count: int = 0
LOGGER.indent()
for inx, data in tqdm(enumerate(input_data)):
    insignals: str = data[0]
    out: str = data[1]
    out_displays: [str] = out.split(" ")
    LOGGER.log(f"Checking data point {inx:3} {insignals} -> {out_displays}")
    LOGGER.indent()
    for display_inx, display in enumerate(out_displays):
        if len(display) in uniqueSegmentAmounts.keys():
            LOGGER.log(f"Display{display_inx} has a simple number.")
            simple_count += 1
    LOGGER.unindent()
LOGGER.unindent()
LOGGER.tee(f"SOLVE: Found {simple_count} simple numbers.")


# Write our logs to the output file
LOGGER.dump_log()
