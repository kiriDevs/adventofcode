INPUT_PATH = "../day01.in"
OUTPUT_PATH = "./part2.out"

with open("../../_common/logger.py", "r") as logger_module:
    exec(logger_module.read())
LOGGER = Logger(OUTPUT_PATH)

DOWN = ")"

from tqdm import tqdm

with open("../day01.in", "r") as input_file:
  INPUT_TEXT = input_file.read()
  INPUT_TEXT = INPUT_TEXT.strip()

current_floor: int = 0


def step(character: str):
    global current_floor
    if character == DOWN:
        LOGGER.log(f"char '{character}' == DOWN '{DOWN}' - Going down a floor.")
        current_floor -= 1
    else:
        LOGGER.log(f"char '{character}' != DOWN '{DOWN}' - Going   up a floor.")
        current_floor += 1


def isInCellar() -> bool:
    global current_floor
    
    isInCellar = current_floor < 0
    if not isInCellar:
        LOGGER.log(f"Floor {current_floor} >= 0: true - Continue.")
    else: 
        LOGGER.log(f"Floor {current_floor} >= 0: false - Exit.")

    return current_floor < 0


def interpret(character) -> bool:  # true / false: whether to continue
    global current_floor
    LOGGER.log(f"Proceeding with char '{character}' from {current_floor}:")

    LOGGER.indent()
    step(character)
    doContinue: bool = not isInCellar()
    LOGGER.unindent()

    return doContinue


def stepThrough(text: str) -> int:  # The INDEX of where we go into the cellar
    global current_floor
    current_floor = 0

    for indx in tqdm(range(len(text))):
        char: str = text[indx]
        LOGGER.log(f"Processing char {char} at index {indx}")

        LOGGER.indent()
        shallContinue: bool = interpret(char)
        LOGGER.unindent()

        if not shallContinue:
            LOGGER.log(f"Exiting.")
            return indx


LOGGER.indent()
cellar_index: int = stepThrough(INPUT_TEXT)
cellar_place: int = cellar_index + 1
LOGGER.unindent()

LOGGER.tee()
LOGGER.tee(f"Stopped at index: {cellar_index}")
LOGGER.tee(f"Santa goes below 0 for the 1st time with char {cellar_place}!")

LOGGER.dmp()
exit(0)
