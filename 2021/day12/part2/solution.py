from tqdm import tqdm

INPUT_PATH: str = "../input" #.example"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)


def recurse(into: str, existing_path: [str], doublesmall: str):
    my_path: [str] = existing_path.copy()
    my_path.append(into)

    if into == "end":
        if not my_path in PATHS:
            PATHS.append(my_path)
        return

    am_small: bool = into.islower()
    can_be_ds: bool = doublesmall == "" and am_small
    ds_available: bool = existing_path.count(doublesmall) <= 1 and not can_be_ds

    my_connections: [str] = CONNECTIONS[into]

    possible_next_steps: [str] = []

    for connection in my_connections:
        if connection.isupper():
            possible_next_steps.append(connection)
            continue
        # Remaining: Only small caves
        if existing_path.count(connection) == 0:
            possible_next_steps.append(connection)
            continue
        # Remaining: Only small caves we are entering for the 2nd+ time
        if connection == doublesmall:
            # Only the doublesmall
            if existing_path.count(connection) == 1:
                # Only the doublesmall we have only been to once
                possible_next_steps.append(connection)
                continue
            # Remaining: Doublesmall we've been to 2 times already
        # Remaining: Small caves we are entering for the 3rd+ time

    if len(possible_next_steps) == 0:
        if not my_path in PATHS:
            PATHS.append(my_path)
    else:
        for next_step in possible_next_steps:
            if not can_be_ds:
                recurse(next_step, my_path, doublesmall)
            else:
                recurse(next_step, my_path, "")
                recurse(next_step, my_path, into)


CONNECTIONS: dict = {}
PATHS: [[str]] = []

LOGGER.tee("Processing input...")
LOGGER.indent()
with open(INPUT_PATH, "r") as infile:
    inlines: [str] = infile.read().strip().split("\n")
LOGGER.log(f"Read {len(inlines)} input lines.")
for lineinx, inline in enumerate(inlines):
    LOGGER.log(f"Line {lineinx}: {inline}")
    constart, conend = inline.split("-")
    if constart not in CONNECTIONS.keys():
        CONNECTIONS[constart] = []
    if conend not in CONNECTIONS.keys():
        CONNECTIONS[conend] = []
    CONNECTIONS[constart].append(conend)
    CONNECTIONS[conend].append(constart)

LOGGER.unindent()
LOGGER.tee(f"Processed {len(inlines)} input lines.")
LOGGER.log(CONNECTIONS)

for start_connection in tqdm(CONNECTIONS["start"]):
    recurse(start_connection, ["start"], "")

deletions: [int] = []
for pathinx, path in enumerate(PATHS):
    lastinx: int = len(path) - 1
    if not path[lastinx] == "end":
        deletions.append(pathinx)
deletions.sort()
while len(deletions) > 0:
    deletion: int = deletions.pop()
    del PATHS[deletion]

LOGGER.tee(f"SOLVE: There are {len(PATHS)} paths.")
LOGGER.log(PATHS)


# Write our logs to the output file
LOGGER.dump_log()
