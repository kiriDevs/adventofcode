from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Reading input...")
with open(INPUT_PATH, "r") as input_file:
    input_lines = input_file.read().strip().split("\n")
instructions = [ins.strip() for ins in tqdm(input_lines)]
LOGGER.tee(f"Successfully read {len(input_lines)} lines.")
LOGGER.tee()

horizontal: int = 0
depth: int = 0

LOGGER.tee("Rrocessing route code...")
LOGGER.indent()
for ins_inx in tqdm(range(len(instructions))):
    ins: str = instructions[ins_inx]
    ins_prts: [str] = ins.split(" ")
    ins_name: str = ins_prts[0]
    ins_value: int = int(ins_prts[1])
    ins_repr: str = f"{ins_inx:04}: {str.ljust(ins_name, 7)}({ins_value:02}) - "

    if ins_name == "up":
        old: int = depth
        depth -= ins_value
        LOGGER.log(ins_repr + f"depth {old:04} -> {depth:04}")
    elif ins_name == "down":
        old: int = depth
        depth += ins_value
        LOGGER.log(ins_repr + f"depth {old:04} -> {depth:04}")
    elif ins_name == "forward":
        old: int = horizontal
        horizontal += ins_value
        LOGGER.log(ins_repr + f"horiz {old:04} -> {horizontal:04}")
    else:
        LOGGER.tee(ins_repr + "Skipping invalid instruction.")
LOGGER.unindent()
LOGGER.tee(f"Done. Horizontal: {horizontal} | Depth: {depth}")
LOGGER.tee(f"Solution: {horizontal*depth}")

# Write our logs to the output file
LOGGER.dump_log()
