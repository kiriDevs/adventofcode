from wtslog import Logger

LOG: Logger = Logger("part1.output")

with open("input", "r") as input_file:
    input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]

calibration_values: [int] = []
for line_inx, line in enumerate(input_lines):
    LOG.log(f"Line {line_inx:03}")
    LOG.indent()
    LOG.log(line)

    first_digit: int = -1
    last_digit: int = -1
    LOG.indent()
    for i in range(len(line)):
        char: str = line[i]
        try:
            digit: int = int(char)
            if first_digit == -1:
                first_digit = digit
                LOG.log(f"first={digit}")
            last_digit = digit
            LOG.log(f"last={digit}")
        except ValueError:
            LOG.log(f"{char} is not a digit")
    LOG.unindent()
    calibration_value: int = int(f"{first_digit}{last_digit}")
    LOG.log(f"Calibration value is {calibration_value}")
    calibration_values.append(calibration_value)
    LOG.unindent()

solution: int = sum(calibration_values)
LOG.tee(f"SOLVE: {solution}")
LOG.dump_log()
