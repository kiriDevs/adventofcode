from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

# Task-Specific Constants
SIMULATION_STEP_COUNT: int = 100

LOGGER.tee("Processing input...")
with open(INPUT_PATH, "r") as infile:
    inlines: [str] = infile.read().strip().split("\n")
ingrid: [[int]] = []
for inline in inlines:
    l: [int] = []
    for c in inline:
        l.append(int(c))
    ingrid.append(l)
totalcount: int = sum([len(l) for l in ingrid])
LOGGER.tee(f"Successfully read {len(ingrid)} lines with {totalcount} numbers.")

LOGGER.tee()

LOGGER.tee(f"Simulating {SIMULATION_STEP_COUNT} steps...")
LOGGER.indent()
flashcount: int = 0
for stepinx in tqdm(range(SIMULATION_STEP_COUNT)):
    LOGGER.log(f"Starting step {stepinx+1}/{SIMULATION_STEP_COUNT}")
    LOGGER.indent()
    stepflashes: [(int, int)] = []
    flashqueue: [(int, int)] = []
    LOGGER.log("Increasing octopusses")
    #LOGGER.indent()
    for y, line in enumerate(ingrid):
        for x, octo in enumerate(line):
            new_value: int = octo + 1
            ingrid[y][x] = new_value
            if new_value > 9:
                flashqueue.append((x, y))
    #LOGGER.unindent()
    LOGGER.log("Octopusses increased.")
    LOGGER.log("Flashing octopusses...")
    LOGGER.indent()
    while len(flashqueue) > 0:
        now_flashing: (int, int) = flashqueue.pop()
        now_x: int = now_flashing[0]
        now_y: int = now_flashing[1]
        LOGGER.log(f"Processing {now_x:2}|{now_y:2}")
        LOGGER.indent()
        if now_flashing in stepflashes:
            LOGGER.log("SKIP: This octopus already flashed in this step.")
            LOGGER.unindent()
            continue
        LOGGER.log(f"Processing neighbours...")
        LOGGER.indent()
        stepflashes.append(now_flashing)
        neighbours: [(int, int)] = []
        neighbours.append((now_x-1, now_y-1))
        neighbours.append((now_x, now_y-1))
        neighbours.append((now_x+1, now_y-1))
        neighbours.append((now_x-1, now_y))
        # neighbours.append((now_x, nowy))
        neighbours.append((now_x+1, now_y))
        neighbours.append((now_x-1, now_y+1))
        neighbours.append((now_x, now_y+1))
        neighbours.append((now_x+1, now_y+1))
        for neigh_x, neigh_y in neighbours:
            LOGGER.log(f"{neigh_x}|{neigh_y}")
            if (
                (neigh_x >= len(ingrid[0]))
                or (neigh_y >= len(ingrid))
                or (neigh_x < 0)
                or (neigh_y < 0)
            ):
                LOGGER.indent()
                LOGGER.log("SKIP: Index out of bounds.")
                LOGGER.unindent()
                continue
            ingrid[neigh_y][neigh_x] = ingrid[neigh_y][neigh_x] + 1
            if ingrid[neigh_y][neigh_x] > 9:
                flashqueue.append((neigh_x, neigh_y))
        LOGGER.unindent()
        LOGGER.unindent()
    LOGGER.unindent()
    LOGGER.log(f"Flashed {len(stepflashes)} octopusses")
    LOGGER.log("Resetting flashed octopusses...")
    LOGGER.indent()
    for flash in stepflashes:
        flashx: int = flash[0]
        flashy: int = flash[1]
        ingrid[flashy][flashx] = 0
        LOGGER.log(f"{flashx:2} {flashy:2}")
    LOGGER.unindent()
    LOGGER.log(f"Reset {len(stepflashes)} octopusses to 0.")
    flashcount += len(stepflashes)
    LOGGER.unindent()
    LOGGER.log(f"There were {len(stepflashes)} flashes this step.")
    LOGGER.unindent()
LOGGER.unindent()
LOGGER.tee(f"SOLVE: There were {flashcount} flashes in total.")

# Write our logs to the output file
LOGGER.dump_log()
