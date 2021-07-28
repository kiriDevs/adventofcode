# Import external libraries
from tqdm import tqdm
from typing import List, Union

# Define logging features
OUTPUT_PATH: str = "part_one.out"
LOG: List[str] = []

INDENT: int = 0
INDENT_STEPS: int = 2


# Create logging functions
def indent():
    global INDENT
    global INDENT_STEPS

    INDENT += INDENT_STEPS


def unindent():
    global INDENT
    global INDENT_STEPS

    INDENT -= INDENT_STEPS
    

def get_indent():
    global INDENT

    indentation: str = ""
    for _ in range(INDENT):
        indentation += " "
    return indentation


def log(what: str = ""):
    global LOG

    if type(what) is not str:
        what = str(what)

    LOG.append(get_indent() + what)


def indent_print(what: str = ""):
    if type(what) is not str:
        what = str(what)

    print(get_indent() + what)


def print_log(what: str = ""):
    indent_print(what)
    log(what)


def save_log():
    global LOG
    global OUTPUT_PATH

    log_string: str = "\n".join(LOG)
    with open(OUTPUT_PATH, "w") as output_file:
        output_file.write(log_string)

    print()
    print(f"Successfully wrote log to {OUTPUT_PATH}.")


# Create some helpful functions
class Statement:
    def __init__(self, label: str, value: int, max_runs: int):
        self.label: str = label
        self.value: int = value
        self.max_runs: int = max_runs
        self.times_run: int = 0

    def __str__(self):
        return(str({
            "label": self.label,
            "value": self.value,
            "max_runs": self.max_runs,
            "times_run": self.times_run
        }))


class Emulator:
    def __init__(self, code: List[Statement] = []):
        self.state: dict = {}
        self.state["COUNTER"] = 0
        self.state["ACCUMULATOR"] = 0

    def __str__(self):
        return f"Emulator Dump: {self.state}"

    def dump(self):
        print_log(self)

    def execute(self, statement:Statement, num:Union[int, None] = None) -> bool:
        statement_token: str = f"{statement.label}|{statement.value}"

        # Make sure the statement is allowed to run
        if statement.times_run >= statement.max_runs:
            print_log(f"CRITICAL: Would execute {statement_token} again!")
            return False

        # Actually interpret the statement
        if statement.label == "jmp":
            cou_before: int = self.state["COUNTER"]
            self.state["COUNTER"] += statement.value
            cou_after: int = self.state["COUNTER"]

            log(f"{statement_token}: {cou_before} -> {cou_after}")
        elif statement.label == "acc":
            acc_before: int = self.state["ACCUMULATOR"]
            self.state["ACCUMULATOR"] += statement.value
            acc_after: int = self.state["ACCUMULATOR"]

            log(f"{statement_token}: {acc_before} -> {acc_after}")
        elif statement.label == "nop":
            log(f"{statement_token}: Ignored")

        # Normal incrementation; doesn't apply when 'jmp' was called
        if statement.label != "jmp":
            self.state["COUNTER"] += 1

        # Update statement and return
        statement.times_run += 1

        return True


EMULATOR: Emulator = Emulator()


# Read our input
INPUT_PATH: str = "day08.in"
with open(INPUT_PATH, "r") as input_file:
    raw_input = input_file.read()
INPUT_LINES = raw_input.split("\n")
print_log(f"Read {len(INPUT_LINES)} lines from {INPUT_PATH}.")

# Remove empty lines from INPUT_LINES
print_log("Starting processing and cleaning input.")
indent()

deleted_lines: int = 0
for line_index in tqdm(range(len(INPUT_LINES))):
    # Check if we are already done because of previously deleted lines
    if line_index >= len(INPUT_LINES):
        break  # We are done

    input_line = INPUT_LINES[line_index]
    if len(input_line.strip()) == 0:
        log(f"Removing line {line_index+deleted_lines+1}: Empty.")
        del INPUT_LINES[line_index]
        deleted_lines += 1

unindent()
print_log(f"Left {len(INPUT_LINES)} lines intact.")

print_log()

# Translate input lines into statements
print_log("Parsing input into statement objects...")
indent()

EMU_STATEMENTS: List[Statement] = []
for input_line in tqdm(INPUT_LINES):
    line_parts = input_line.split(" ")
    label = line_parts[0]
    value = int(line_parts[1])

    statement = Statement(label, value, 1)
    EMU_STATEMENTS.append(statement)
    log(statement)

unindent()
print_log(f"Successfully parsed {len(EMU_STATEMENTS)} statements.")

print_log()

# Start executing the code
print_log("Executing code...")

continue_running: bool = True
while continue_running:
    statement_index: int = EMULATOR.state["COUNTER"]
    statement: Statement = EMU_STATEMENTS[statement_index]

    indent()
    continue_running = EMULATOR.execute(statement)
    unindent()

if continue_running:
    print_log("Code ran completely.")
else:
    print_log("Reached breakpoint.")
print_log("Dumping emulator.")

indent()
EMULATOR.dump()
unindent()

save_log()
