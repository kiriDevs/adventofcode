from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)


def recurse(into, existing_path):
    my_path: [str] = existing_path.copy()
    my_path.append(into)

    if into == "end":
        PATHS.append(my_path)
        return

    my_connections: [str] = CONNECTIONS[into]

    possible_next_steps: [str] = []
    for connection in my_connections:
        if connection.islower() and connection in existing_path:
            continue;
        possible_next_steps.append(connection);
    if len(possible_next_steps) == 0:
        PATHS.append(my_path)
    else:
        for next_step in possible_next_steps:
            recurse(next_step, my_path)


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

for start_connection in CONNECTIONS["start"]:
    recurse(start_connection, ["start"])

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
