from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Loading input...")
LOGGER.indent()
with open(INPUT_PATH, "r") as infile:
    input_lines = [list(a) for a in infile.read().strip().split("\n")]
for inx, line in enumerate(input_lines):
    input_lines[inx] = [int(a) for a in line]
if min([len(a) for a in input_lines]) != max([len(a) for a in input_lines]):
    LOGGER.tee("Malformed input. Expected a square field.")
    exit(1)
LOGGER.unindent()
LOGGER.tee(f"Loaded {len(input_lines)} lines.")

LOGGER.tee()

low_points: [(int, int)] = []
LOGGER.tee("Searching for low points...")
LOGGER.indent()
for line_inx, line in tqdm(enumerate(input_lines)):
    LOGGER.log(f"Checking line {line_inx}...")
    lowp_before: int = len(low_points)
    LOGGER.indent()
    for col_inx, col in enumerate(line):
        if all([
            (
                (col_inx == 0) or
                (not input_lines[line_inx][col_inx-1] <= col)
            ), (
                (col_inx == len(line)-1) or
                (not input_lines[line_inx][col_inx+1] <= col)
            ), (
                (line_inx == 0) or
                (not input_lines[line_inx-1][col_inx] <= col)
            ), (
                (line_inx == len(input_lines)-1) or
                (not input_lines[line_inx+1][col_inx] <= col)
            )
        ]):
            low_points.append((line_inx, col_inx))
            LOGGER.log(f"Detected low point at y{line_inx:2}|x{col_inx:2}")
    LOGGER.unindent()
    LOGGER.log(f"Found {len(low_points) - lowp_before} new low points")
LOGGER.unindent()
LOGGER.tee(f"Found {len(low_points)} low points.")

LOGGER.tee()

LOGGER.tee("Calculating heat scores...")
LOGGER.indent()
heat_scores: [int] = []
for y, x in tqdm(low_points):
    height: int = input_lines[y][x]
    heat_score: int = height + 1
    heat_scores.append(heat_score)
    LOGGER.log(f"y{y:2}|x{x:2} has a heat score of {heat_score}")
LOGGER.unindent()
LOGGER.tee(f"Added heat scores: {sum(heat_scores)}")

# Write our logs to the output file
LOGGER.dump_log()
