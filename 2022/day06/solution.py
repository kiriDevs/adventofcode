INPUT_PATH: str = "../input"

with open(INPUT_PATH, "r") as input_file:
    signals: [str] = list(input_file.read().strip())


def RESET(buf_len: int):
    global ROTATING_BUFFER_LENGTH
    global rotating_buffer
    global buffer_taint

    ROTATING_BUFFER_LENGTH = buf_len - 1
    rotating_buffer = []
    buffer_taint = []


ROTATING_BUFFER_LENGTH: int = -1
rotating_buffer: [str] = []
buffer_taint: [str] = []


def buffer_shift(new_value: str):
    global ROTATING_BUFFER_LENGTH
    global rotating_buffer

    # Flag buffer if we have a collision inside of the buffer itself
    if new_value in rotating_buffer:
        buffer_taint.append(new_value)

    rotating_buffer.append(new_value)
    if len(rotating_buffer) > ROTATING_BUFFER_LENGTH:
        old_char = rotating_buffer.pop(0)
        if (
            old_char in buffer_taint
            and rotating_buffer.count(old_char) <= 1
        ):  # Buffer is tainted by the signal that is removed
            while old_char in buffer_taint:
                buffer_taint.remove(old_char)


def find_first_marker(marker_length: int) -> int:
    RESET(marker_length)
    for (signal_inx, signal) in enumerate(signals):
        if (
            signal not in rotating_buffer
            and len(rotating_buffer) == ROTATING_BUFFER_LENGTH
            and len(buffer_taint) == 0
        ):
            return (signal_inx + 1)  # +1: Convert index -> amount of characters
        buffer_shift(signal)


print(find_first_marker( 4))  # Part 1
print(find_first_marker(14))  # Part 2