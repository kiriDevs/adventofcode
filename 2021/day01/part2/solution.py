from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

with open(INPUT_PATH, "r") as input_file:
    input_lines: [str] = input_file.read().strip().split("\n")
input_numbers: [int] = [int(line.strip()) for line in input_lines]
LOGGER.tee(f"Read {len(input_numbers)} numbers.")
LOGGER.tee()

#####
# I know that actually dividing it into the theoretical "windows" as suggested
# by the task text is probably not the most efficient way, since there is a lot
# of overlapping numbers, but it runs fine and I think it's neat to do stuff
# as the task specifies it (if reasonable) because it's well-understandable.
#####
LOGGER.tee("Processing numbers into 3-num windows...")
LOGGER.indent()
windows: [[int]] = []
for index in tqdm(range(len(input_numbers))):
    # Skip the cycle if this number is the last or second to last
    if (index in [len(input_numbers)-1, len(input_numbers)-2]):
        continue

    num: int = input_numbers[index]
    next_num: int = input_numbers[index+1]
    next_next: int = input_numbers[index+2]
    window: [int] = [num, next_num, next_next]
    windows.append(window)
LOGGER.unindent()
LOGGER.tee("Done. Dumping windows to log.")
LOGGER.log(windows)
LOGGER.tee()

LOGGER.print("Summing up window values...")
window_values: [int] = [sum(windows[i]) for i in tqdm(range(len(windows)))]

# At this point it's basically just the same as part1
LOGGER.tee("Counting depth increases...")
went_deeper_amount: int = 0
for win_val_index in tqdm(range(len(window_values))):
    window_value: int = window_values[win_val_index]
    if not win_val_index == 0:
        previous: int = window_values[win_val_index-1]
        went_deeper: bool = window_value > previous
        if went_deeper:
            went_deeper_amount += 1
        comp_sign: str = "> " if went_deeper else "<="
        LOGGER.log(
                    f"{win_val_index:04}: "
                    + f"{window_value:05} {comp_sign} {previous:05} "
                    + f"- Deeper: {went_deeper}"
                  )
    else:
        LOGGER.log(
                    f"{win_val_index:04}: {window_value:05}"
                    + "          - First window - OK!"
                  )
LOGGER.tee()
LOGGER.tee(f"Done.")
LOGGER.tee(f"The sonar went deeper {went_deeper_amount} times.")


# Write our logs to the output file
LOGGER.dump_log()
