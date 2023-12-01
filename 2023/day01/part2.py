from wtslog import Logger

LOG: Logger = Logger("part2.output")

DIGIT_MAP: dict[str, str] = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def char_digit(chars: [str]) -> int:
    global DIGIT_MAP
    string: str = "".join(chars)
    for k in DIGIT_MAP.keys():
        v: str = DIGIT_MAP[k]
        if k in string:
            return v
    return -1


with open("input", "r") as input_file:
    input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]

calibration_values: [int] = []
for line_inx, line in enumerate(input_lines):
    LOG.log(f"Line {line_inx:03}")
    LOG.indent()
    LOG.log(line)

    LOG.indent()
    first_digit: int = -1
    last_digit: int = -1
    char_buf: [str] = []
    for i in range(len(line)):
        char: str = line[i]
        digit: int = -1
        try:
            digit = int(char)
            LOG.log(f"Digit: {char}")
            char_buf = []
        except ValueError:
            char_buf.append(char)
            LOG.log(f"{char} is not a digit | {''.join(char_buf)}")

            digit = char_digit(char_buf)
            if digit != -1:  # Found a digit from chars
                LOG.log(f"From chars: {digit}")
                last_char: str = char_buf[len(char_buf) - 1]
                char_buf = [last_char]  # Keep last char for double usages

        if digit != -1:  # Found a digit one way or another
            LOG.indent()
            if first_digit == -1:
                first_digit = digit
                LOG.log(f"first={digit}")
            last_digit = digit
            LOG.log(f"last={digit}")
            LOG.unindent()
    LOG.unindent()
    calibration_value: int = int(f"{first_digit}{last_digit}")
    LOG.log(f"Calibration value is {calibration_value}")
    calibration_values.append(calibration_value)
    LOG.unindent()

solution: int = sum(calibration_values)
LOG.tee(f"SOLVE: {solution}")
LOG.dump_log()
