# Import external modules
from tqdm import tqdm
from typing import List, Union

# Define logging features
OUTPUT_PATH: str = "part_one.out"
LOG: List[str] = []
LOG_INDENT: int = 0
INDENT_STEPS: int = 2


def indent():
    global LOG_INDENT
    global INDENT_STEPS

    LOG_INDENT += INDENT_STEPS


def unindent():
    global LOG_INDENT
    global INDENT_STEPS

    LOG_INDENT -= INDENT_STEPS


def get_indent():
    global LOG_INDENT

    indent: str = ""
    for _ in range(LOG_INDENT):
        indent += " "
    return indent


def indented_print(what: str = ""):
    if type(what) is not str:
        what = str(what)

    print(get_indent() + what)


def log(what: str = ""):
    global LOG

    if type(what) is not str:
        what = str(what)

    LOG.append(get_indent() + what)


def print_log(what: str = ""):
    indented_print(what)
    log(what)


def save_log():
    global LOG

    output_string = "\n".join(LOG)
    with open(OUTPUT_PATH, "w") as output_file:
        output_file.write(output_string)

    print()
    print(f"Successfully wrote log to {OUTPUT_PATH}.")


# Read our input
INPUT_PATH: str = "day09.in"
with open(INPUT_PATH, "r") as input_file:
    raw_input = input_file.read()
raw_input = raw_input.strip()  # This should also remove empty lines
INPUT_LINES = raw_input.split("\n")
print_log(f"Read {len(INPUT_LINES)} lines from {INPUT_PATH}.")

print_log()

print_log("Converting values to integers.")

INPUT_NUMBERS: List[int] = []
for line_index in tqdm(range(len(INPUT_LINES))):
    number_string: str = INPUT_LINES[line_index]
    number: int = int(number_string)
    INPUT_NUMBERS.append(number)

print_log("Done.")


def find_summands(number_index: int, in_numbers: List[int]):
    search_number: int = INPUT_NUMBERS[number_index]
    for index1 in range(len(in_numbers)):
        for index2 in range(len(in_numbers)):
            if index1 == index2:
                continue
            else:
                number1: int = in_numbers[index1]
                number2: int = in_numbers[index2]
                if number1 + number2 == search_number:
                    return [number1, number2]
    return None


def number_is_valid(check_index: int) -> bool:
    check_number = INPUT_NUMBERS[check_index]
    log(f"Checking validity of {check_number} in line {check_index+1}...")
    indent()

    if check_index in range(25):
        # We are still in the preamble
        log("Preamble")
        unindent()
        return True
    
    log(f"Gathering 25 numbers before index {check_index}...")
    last_twenty_five: List[int] = []
    indent()
    for offset in range(1, 26):
        index: int = check_index - offset
        number: int = INPUT_NUMBERS[index]
        last_twenty_five.insert(0, number)
        log(f"Found {number} in line {index+1} (index {index}).")
    unindent()
    log(f"Gathered numbers {last_twenty_five}.")

    log(f"Searching for summands...")
    indent()
    summands = find_summands(check_index, last_twenty_five)
    unindent()

    if summands is None:
        log(f"Couldn't find possible summands.")
    else:
        log(f"Found summands: {summands}")

    unindent()
    if summands is None:
        log(f"Invalid.")
    else:
        log(f"Valid.")
    return summands is not None


for number_index in tqdm(range(len(INPUT_NUMBERS))):
    input_number: int = INPUT_NUMBERS[number_index]
    is_valid: bool = number_is_valid(number_index)
    log(f"Number {number_index+1} ({input_number}) is valid: {is_valid}")
    if not is_valid:
        unindent()
        print_log(f"{input_number} is the first invalid number!")
        break

save_log()
