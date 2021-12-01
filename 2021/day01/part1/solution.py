from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

with open(INPUT_PATH, "r") as input_file:
    input_lines: [str] = input_file.read().strip().split("\n")
input_numbers: [int] = [int(line.strip()) for line in input_lines]

LOGGER.tee("Processing numbers...")
LOGGER.indent()
went_deeper_amount: int = 0

for index in tqdm(range(len(input_numbers))):
    number: int = input_numbers[index]
    if not index == 0:
        previous: int = input_numbers[index-1]
        went_deeper: bool = number > previous
        if went_deeper:
            went_deeper_amount += 1
        comp_sign: str = ">" if went_deeper else "<="
        LOGGER.log(f"{number} {comp_sign} {previous} - Deeper: {went_deeper}")
    else:
        LOGGER.log(f"{number} - First number, OK!")
        continue

LOGGER.unindent()
LOGGER.tee("Done.")
LOGGER.tee()
LOGGER.tee(f"The sonar went deeper {went_deeper_amount} times.")

# Write our logs to the output file
LOGGER.dump_log()
