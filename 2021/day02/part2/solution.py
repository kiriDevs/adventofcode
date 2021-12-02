from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Loading input...")
with open(INPUT_PATH, "r") as input_file:
    input_lines: [str] = input_file.read().strip().split("\n")
instructions: [str] = [line.strip() for line in tqdm(input_lines)]
LOGGER.tee(f"Successfully loaded {len(instructions)} instructions.")

horizontal: int = 0
depth: int = 0
aim: int = 0

LOGGER.tee("Processing instructions...")
LOGGER.indent()
for ins_inx in tqdm(range(len(instructions))):
    ins: str = instructions[ins_inx]
    ins_prts: [str] = ins.split(" ")
    ins_name: str = ins_prts[0]
    ins_val: int = int(ins_prts[1])
    ins_repr: str = f"{ins_inx:04}: {str.ljust(ins_name, 7)}({ins_val:02}) - "

    if ins_name == "down":
        old: int = aim
        aim += ins_val
        LOGGER.log(ins_repr + f"aim   {old:06} -> {aim:06}")
    elif ins_name == "up":
        old: int = aim
        aim -= ins_val
        LOGGER.log(ins_repr + f"aim   {old:06} -> {aim:06}")
    elif ins_name == "forward":
        old_h: int = horizontal
        old_d: int = depth
        horizontal += ins_val
        depth += (ins_val * aim)
        LOGGER.log(
            ins_repr
            + f"horiz {old_h:06} -> {horizontal:06} | depth {old_d:06} -> {depth:06}"
        )
    else:
        LOGGER.tee(ins_repr + "Skipping invalid instruction.")
LOGGER.unindent()
LOGGER.tee(f"Done. Horizontal: {horizontal} | Depth: {depth}")
LOGGER.tee(f"Solution: {horizontal*depth}")

# Write our logs to the output file
LOGGER.dump_log()
